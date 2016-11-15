//
// Score.java
// $Id: Score.java 7 2008-01-27 21:16:28Z melamed $
//
// written by Ryan Green, Joseph P. Turian, I. Dan Melamed, and Luke Shen
// Copyright (c) 2003, New York University
//
// Wrapper routines for creating and scoring a bitext
//

import java.io.*;

import java.math.*;

import java.util.*;

public class Score {
    static private double _exponent = 0;
    static private double _sizeX = 0;
    static private double _sizeYMean = -1;

    static public void init(double exponent) {
        _exponent = exponent;
    }

    static public double processSeg(String[] refStrs, String tstStr, PrintWriter hitWriter, PrintWriter runWriter) {
        StringTokenizer tstTokize = new StringTokenizer(tstStr);
        LinkedList tstList = new LinkedList();

        while (tstTokize.hasMoreTokens()) {
            String tstToken = tstTokize.nextToken();

            //System.out.println("tstToken: " + tstToken);
            tstList.addLast(tstToken);
        }

        _sizeX = tstList.size();

        LinkedList refList = new LinkedList();
        _sizeYMean = 0;

        for (int i = 0; i < refStrs.length; i++) {
            int cnt = 0;
            StringTokenizer refTokize = new StringTokenizer(refStrs[i]);

            while (refTokize.hasMoreTokens()) {
                String refToken = refTokize.nextToken();

                //System.out.println("refToken: " + refToken);
                refList.addLast(refToken);
                cnt++;
            }

            _sizeYMean += cnt;
            refList.addLast("REFERENCE BREAK");
        }

        _sizeYMean = ((float) 1.0 * _sizeYMean) / refStrs.length;

	Bitext bitext = new Bitext(refList, tstList, hitWriter, runWriter);

	//System.out.println(_sizeX + " " + _sizeYMean);

        return bitext.score(_exponent, Math.min(_sizeX, _sizeYMean));
    }

    static public double getSizeX() {
        return _sizeX;
    }

    static public double getSizeYMean() {
        return _sizeYMean;
    }

    static public double getExponent() {
        return _exponent;
    }
}
