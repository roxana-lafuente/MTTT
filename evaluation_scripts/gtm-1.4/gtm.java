// Main routine for scoring text matches
//
import java.io.*;

import java.lang.reflect.*;

import java.util.*;
import java.util.regex.*;


public class gtm {
    static public boolean verbose = false;

    // Print command line options and exit
    private static void printUsage() {
        System.err.println("Usage: java gtm\t\t\t\t\t\\\n" +
            "\t[-v]\t\t\t\t\t\\\n" +
	    "\t[-e exponent]\t\t\t\t\\\n" +
            "\t[+s|-s|--scoresegs|--noscoresegs]\t\\\n" +
            "\t[+d|-d|--scoredocs|--noscoredocs]\t\\\n" +
	    "\t[-t| --textin]\t\t\t\t\\\n" +
	    "\t[-l| --lineFile]\t\t\t\t\\\n" +
	    "\t[--dumphits file]\t\t\t\t\\\n" +
	    "\t[--dumpruns file]\t\t\t\t\\\n" +
            "\ttestfile referencefile(s)\n\n" +
            "Please see the README for help with these options.");
        System.exit(-1);
    }

    private static void printDocumentScore(String tstDoc, double score,
        double xsum, double ysum) {
        double prc = 0;
        double rcl = 0;
        double fms = 0;

        if (xsum != 0) {
            prc = score / xsum;
        }

        if (ysum != 0) {
            rcl = score / ysum;
        }

        if ((prc + rcl) > 0) {
            fms = (2 * (prc * rcl)) / (prc + rcl);
        }

        System.out.println(tstDoc + " " + fms);

        if (verbose) {
            System.out.println("document: " + tstDoc);
            System.out.println("\ttotal (maximum matching)^(1/exponent) = " +
                score);
            System.out.println("\ttotal mean length of reference segments = " +
                ysum);
            System.out.println("\ttotal length of test segments = " + xsum);
            System.out.println("\tdocument precision = " + prc);
            System.out.println("\tdocument recall = " + rcl);
            System.out.println("\tdocument f-measure = " + fms);
        }
    }

    private static String wrapText(String plainText, String lineFile) {
	// take in the name of a plain text file 
	// create a temp file with the wrapped version
	// return the path to the temp file

	String openDoc = "<doc docid=\"sampledoc-0\" sysid=\"ref1\">\n";
	String closeDoc = "</doc>\n";
	String openSeg = "<seg id=";
	String closeSeg = "</seg>\n";
	Integer count = 0;
	String wraped = openDoc + openSeg + plainText + closeSeg + closeDoc;
	String tName = new String();



	// Create temp file to write the wrapped file to.

	try {
	    File temp = File.createTempFile("wraptxt", ".tmp");
	    temp.deleteOnExit();
	    BufferedWriter out = new BufferedWriter(new FileWriter(temp));
	    out.write(openDoc);

	    BufferedReader in = new BufferedReader(new FileReader(new File(plainText)));
	    if(lineFile.equals("")) {
		String line = in.readLine();
		count = count + 1;
		while (line != null) {
//		    if (line.trim().equals("")) {
//			line = in.readLine();
//			continue;
//		    }
		    out.write(openSeg + count + ">");
		    out.write(line);
		    out.write(closeSeg);
		    line = in.readLine();
		    count++;
		}
	    } else {
		// compensates for line offsets between the refFile and tstFile
		String line = in.readLine();
		// TODO: check that number of lines in tstFile is the same as number of lines in lineFile
		BufferedReader lin = new BufferedReader(new FileReader(new File(lineFile)));
		String lcount = lin.readLine();
		while (line != null) {
		    if(lcount != null) {
			count = new Integer(lcount).intValue();
			out.write(openSeg + count + ">");
			out.write(line);
			out.write(closeSeg);
			line = in.readLine();
			lcount = lin.readLine();
		    }
		    else {
			System.err.println("Different number of entries in " + lineFile + " and " + plainText);
			System.err.println("Exiting...");
			System.exit(-1);
		    }
		}
	    }
	    out.write(closeDoc);
	    tName = temp.getPath();
	    out.close();
	    
	    
	} catch (IOException e) {
	    e.printStackTrace();
	    System.err.println("Exiting...");
	    System.exit(-1);
	}
	return tName;
    }


    public static void main(String[] args) {
        double exponent = 1.0;
        boolean internal_debug = false;
        boolean showsegs = false;
        boolean showdocs = true;
	boolean textin = false;
	String  lineFile = "";
	String  hitFile  = "";
	String  runFile  = "";
	
	PrintWriter hitWriter = null;
	PrintWriter runWriter = null;

	// set the file encoding to LATIN alphabet
	// if you need a different encoding replace it here
	try {
	    System.setProperty("file.encoding","ISO8859_15");
	} catch (Exception e) {
	    System.err.println("Unable to set the encoding.");
	    System.err.println("Exiting...");
	}
	    
        int arg = 0;

        if (args.length < 2) {
            printUsage();
        }

        while ((args[arg].charAt(0) == '-') || (args[arg].charAt(0) == '+')) {
            if (args[arg].equals("-v")) {
                verbose = true;
                arg++;
            } else if (args[arg].equals("-e")) {
                exponent = Double.parseDouble(args[arg + 1]);
                arg += 2;
	    }
	    else if (args[arg].equals("--lineFile") ||
		     args[arg].equals("-l")) {
		lineFile = args[arg + 1];
		arg += 2;
	    } else if (args[arg].equals("--scoresegs") ||
                    args[arg].equals("+s")) {
                showsegs = true;
                arg++;
            } else if (args[arg].equals("--noscoresegs") ||
                    args[arg].equals("-s")) {
                showsegs = false;
                arg++;
            } else if (args[arg].equals("--scoredocs") ||
                    args[arg].equals("+d")) {
                showdocs = true;
                arg++;
            } else if (args[arg].equals("--noscoredocs") ||
                    args[arg].equals("-d")) {
                showdocs = false;
                arg++;
	    } else if (args[arg].equals("--textin") ||
		       args[arg].equals("-t")) {
		textin = true;
		arg++;
	    } else if(args[arg].equals("--dumphits") ||
		      args[arg].equals("-dh")) {
		if(args[arg+1].startsWith("-")) {
		    printUsage();
		}
		else {
		    hitFile = args[arg+1];
		    arg++;
		}
		arg++;
	    } else if(args[arg].equals("--dumpruns") ||
		      args[arg].equals("-dr")) {
		if(args[arg+1].startsWith("-")) {
		    printUsage();
		}
		else {
		    runFile = args[arg+1];
		    arg++;
		}
		arg++;
	    }
	    
	    else if (args[arg].equals("--internal-debug")) {
		// Parameter for debug output (for developers)
                internal_debug = true;
                arg++;
            } else {
                System.err.println("Unknown command line option \"" +
                    args[arg] + "\"\n");
                printUsage();
            }
        }

        if ((args.length - arg) < 2) {
            printUsage();
        }

	if(!hitFile.equals("")) {
	    try {
		hitWriter = new PrintWriter(new BufferedWriter(new FileWriter(hitFile)));
	    } catch(Exception e) {
		System.err.println("Warning: could not open file for dumping hits");
	    }
	}

	if(!runFile.equals("")) {
	    try {
		runWriter = new PrintWriter(new BufferedWriter(new FileWriter(runFile)));
	    } catch(Exception e) {
		System.err.println("Warning: could not open file for dumping hits");
	    }
	}	

        if (internal_debug) {
	    showdocs = false;
	    showsegs = true;
	    verbose = false;
	}

        String tstFile = args[arg];
        int refFileCnt = args.length - 1 - arg;
        String[] refFiles = new String[refFileCnt];

        if (verbose) {
            System.out.println("program options:");
            System.out.println("\tverbose = on");
            System.out.println("\texponent = " + exponent);
            System.out.println("\tscore segments = " + showsegs);
            System.out.println("\tscore documents = " + showdocs);
            System.out.println("\ttest file = " + tstFile);
            System.out.println("\treference file(s) = ");
        }

        for (int i = 0; i < refFileCnt; i++) {
            refFiles[i] = args[arg + i + 1];

            if (verbose) {
                System.out.println("\t\t" + refFiles[i]);
            }
        }

        Score.init(exponent);

        Vector tstSegs = new Vector();
        Vector[] refSegs = new Vector[refFileCnt];
        Vector tstSegsName = new Vector();
        Vector[] refSegsName = new Vector[refFileCnt];
        Vector tstDocsName = new Vector();
        Vector[] refDocsName = new Vector[refFileCnt];
        String sysName = new String();

        for (int i = 0; i < refFileCnt; i++) {
            refSegs[i] = new Vector();
            refSegsName[i] = new Vector();
            refDocsName[i] = new Vector();
        }

	


        try {
            BufferedReader in;
            Pattern patternDoc = Pattern.compile(
                    "<[dD][oO][cC] [dD][oO][cC][iI][dD]=\"(.*?)\" [sS][yY][sS][iI][dD]=\"(.*?)\">");
            Pattern patternSeg = Pattern.compile("<[sS][eE][gG] [iI][dD]=(.*?)>(.*?)</[sS][eE][gG]>");
            String curDoc = new String();
	    
            for (int i = 0; i < refFileCnt; i++) {

		///////////////////////////////////////////////////////////////////
		// added by ali 08/26/03
		// if the file is a plain text file it needs to be wrapped with sgml
		if (textin) {
		    in = new BufferedReader(new FileReader(new File(wrapText(refFiles[i], ""))));
		} else {
		    in = new BufferedReader(new FileReader(new File(refFiles[i])));
		}
		// was: in = new BufferedReader(new FileReader(new File(refFiles[i])));
		///////////////////////////////////////////////////////////////////
                
                try {
                    String line = in.readLine();

                    while (line != null) {
                        Matcher matcherSeg = patternDoc.matcher(line);

                        if (matcherSeg.find()) {
                            curDoc = matcherSeg.group(1).trim();
                        } else {
                            matcherSeg = patternSeg.matcher(line);

                            if (matcherSeg.find()) {
                                String text = matcherSeg.group(2).trim();
                                refSegs[i].add(text);
                                refSegsName[i].add(matcherSeg.group(1).trim());
                                refDocsName[i].add(curDoc);
                            }
                        }

                        line = in.readLine();
                    }

		    // added by ali 08/26/03 to catch condition where invalid options/input was given
		    if (refSegs[i].size() == 0) {
			System.out.println("No content found, if this was a plain text file please use option -t");
			throw new IOException();
		    }

                } catch (IOException e) {
                    e.printStackTrace();
                    System.err.println("Exiting...");
                    System.exit(-1);
                }
            }

            curDoc = new String("");

	    ///////////////////////////////////////////////////////////////////
	    // added by ali 08/26/03
	    // if the file is a plain text file it needs to be wrapped with sgml
	    if (textin) {
		in = new BufferedReader(new FileReader(new File(wrapText(tstFile, lineFile))));
	    } else {
		in = new BufferedReader(new FileReader(new File(tstFile)));
	    }
	    // was: in = new BufferedReader(new FileReader(new File(tstFile)));
	    ///////////////////////////////////////////////////////////////////
	 

	    




            try {
                String line = in.readLine();

                while (line != null) {
                    Matcher matcherSeg = patternDoc.matcher(line);

                    if (matcherSeg.find()) {
                        curDoc = matcherSeg.group(1).trim();

                        if (sysName.equals("")) {
                            sysName = matcherSeg.group(2).trim();
                        } else if (!sysName.equals(matcherSeg.group(2).trim())) {
                            System.err.println("SYSID mis-match: " + sysName +
                                " vs. " + matcherSeg.group(2).trim());
                        }
                    } else {
                        matcherSeg = patternSeg.matcher(line);

                        if (matcherSeg.find()) {
                            String text = matcherSeg.group(2).trim();
                            tstSegs.add(text);
                            tstSegsName.add(matcherSeg.group(1).trim());
                            tstDocsName.add(curDoc);
                        }
                    }

                    line = in.readLine();
                }
		// added by ali 08/26/03 to catch condition where invalid options/input was given
		if (tstSegs.size() == 0) {
		    System.out.println("No content found, if this was a plain text file please use option -t");
		    throw new IOException();
		}
		
            } catch (IOException e) {
                e.printStackTrace();
                System.err.println("Exiting...");
                System.exit(-1);
            }
        } catch (Exception e) {
            e.printStackTrace();
            System.err.println("Exiting...");
            System.exit(-1);
        }

	Vector linesVec = new Vector();
	System.err.println("lineFile: " + lineFile);
	if(!lineFile.equals("")){
	    try{
		BufferedReader linein;
		linein = new BufferedReader(new FileReader(new File(lineFile)));
		String line = linein.readLine();
		while (line != null) {
		    int i = Integer.parseInt(line);
		    linesVec.add(i-1);
		    line = linein.readLine();
		}
	    }
	    catch (Exception e) {
		e.printStackTrace();
		System.err.println("Exiting...");
		System.exit(-1);
	    }
	}
	else{
	    for(int i = 0; i < tstSegs.size(); i++){
		linesVec.add(i);
	    }
	    
	    for (int i = 0; i < refFileCnt; i++) {
		if (refSegs[i].size() != tstSegs.size()) {
		    System.err.println("Differing number of segments:");
		    System.err.println("\t" + refSegs[i].size() + " in reference: " + refFiles[i]);
		    System.err.println("\t" + tstSegs.size() + " in test: " + tstFile);
		    System.err.println("\tExiting...");
		    System.exit(-1);
		}
	    }
	}

        String[] refs = new String[refFileCnt];

        double score = 0;
        double xsum = 0;
        double ysum = 0;

        for (int i = 0; i < linesVec.size(); i++) {
            String tstDoc = (String) tstDocsName.get(i);
            String tstName = (String) tstSegsName.get(i);

	    // Avoid checking differences in segment ID's
	    // needed in order to allow for 

	    
            for (int j = 0; j < refFileCnt; j++) {
                refs[j] = (String) refSegs[j].get((Integer)linesVec.get(i));
                String refDoc = (String) refDocsName[j].get((Integer)linesVec.get(i));
                String refName = (String) refSegsName[j].get((Integer)linesVec.get(i));

                if (!tstDoc.equals(refDoc)) {
                    System.err.println("Differing document ID's: " + tstDoc +
                        " vs. " + refDoc);
                    System.err.println("Exiting...");
                    System.exit(-1);
                }

                if (!tstName.equals(refName)) {
                    System.err.println("Differing segment ID's: " + tstName +
                        " vs. " + refName);
                    System.err.println("Exiting...");
                    System.exit(-1);
                }
		}

            String tst = (String) tstSegs.get(i);

            if (showdocs && (i != 0) && !tstDoc.equals(tstDocsName.get(i - 1))) {
                printDocumentScore((String) tstDocsName.get(i - 1), score,
							    xsum, ysum);
				   
                score = 0;
                xsum = 0;
                ysum = 0;
            }

            double segscore_orig = Score.processSeg(refs, tst, hitWriter, runWriter);
            double segscore = Math.pow(segscore_orig, 1 / exponent);
            score += segscore;
            xsum += Score.getSizeX();
            ysum += Score.getSizeYMean();

            if (showsegs) {
                double segxsum = Score.getSizeX();
                double segysum = Score.getSizeYMean();
                double prc = 0;
                double rcl = 0;
                double fms = 0;

                if (segxsum != 0) {
                    prc = segscore / segxsum;
                }

                if (segysum != 0) {
                    rcl = segscore / segysum;
                }

                if ((prc + rcl) > 0) {
                    fms = (2 * (prc * rcl)) / (prc + rcl);
                }


                if (internal_debug)
                    System.out.println(sysName + " " + tstDoc + "-" + tstName + " " + segscore_orig + " " + Score.getSizeX() + " " + Score.getSizeYMean());
		else 
                    System.out.println(tstDoc + " " + tstName + " " + fms);

                if (verbose) {
                    System.out.println("document: " + tstDoc + ", segment: " +
                        tstName);
                    System.out.println("\tmaximum matching = " + segscore_orig);
                    System.out.println("\t(maximum matching)^(1/exponent) = " +
                        segscore);
                    System.out.println("\tmean length of reference segments = " +
                        segysum);
                    System.out.println("\tlength of test segment = " + segxsum);
                    System.out.println("\tsegment precision = " + prc);
                    System.out.println("\tsegment recall = " + rcl);
                    System.out.println("\tsegment f-measure = " + fms);
                }
            }
        }

        if (showdocs) {
            printDocumentScore((String) tstDocsName.get(tstSegs.size() - 1),
                score, xsum, ysum);
        }

	if(hitWriter != null) {
	    hitWriter.close();
	}
	if(runWriter != null) {
	    runWriter.close();
	}
    }
}
