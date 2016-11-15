//
// Bitext.java
// $Id: Bitext.java 7 2008-01-27 21:16:28Z melamed $
//
// written by Ryan Green, Joseph P. Turian, I. Dan Melamed, and Luke Shen
// Copyright (c) 2003, New York University
//
// Core routines for creating and scoring a bitext
//

import java.io.*;
import java.util.*;
import java.lang.Object.*;

public class Bitext {

    private HashSet _hits;
    private int _X;
    private int _Y;
    private SortedSet _runs = new TreeSet();

    private PrintWriter hitWriter = null;
    private PrintWriter runWriter = null;

    public Bitext(LinkedList refList, LinkedList tstList, PrintWriter hitWriter, PrintWriter runWriter) {
        _hits = new HashSet();

        ListIterator refListI = refList.listIterator(0);

        _X = refList.size();
        _Y = tstList.size();

	this.hitWriter = hitWriter;
	this.runWriter = runWriter;



        while (refListI.hasNext()) {
            String refToken = ((String) refListI.next());
            ListIterator tstListI = tstList.listIterator(0);
	    
            while (tstListI.hasNext()) {
		if (refToken.equals((String) tstListI.next())) {
		    
                    int[] h = new int[2];
                    h[0] = tstListI.previousIndex();
                    h[1] = refListI.previousIndex();

                    Integer hi = p2i(h);

                    //System.err.println("hit " + h[0] + " " + h[1] + " " + hi);
                    _hits.add(hi);
		    if(hitWriter != null) {
			hitWriter.print("(" + h[0] + " " + h[1] + ") ");
		    }
                }
            }
        }

	if(hitWriter != null) {
	    hitWriter.println();
	}

        Iterator iterator = _hits.iterator();
        while (iterator.hasNext()) {
            Integer h = (Integer)iterator.next();
            addHitRuns(h);
        }

//for debug
/*
        Iterator iter = _runs.iterator();
        while (iter.hasNext()) {
            Run run = (Run)iter.next();
            System.out.println(run);
        }
        System.out.println("......");	
*/
    }

    // add all runs originating at hit h
    private void addHitRuns(Integer h) {
        int len = 1;
        if (h.intValue() == -1) {
            return;
        }
        Integer hr = rightmost(h);
        len = runlength(h, hr);

        for (int l=1; l <= len; l++) {
            Run run = new Run(h, l);
            _runs.add(run);
        } 
    }

    // Convert a point to an Integer
    private Integer p2i(int[] h) throws ArrayIndexOutOfBoundsException {
        if ((h[0] < 0) || (h[1] < 0)) {
            throw new ArrayIndexOutOfBoundsException();
        } else if ((h[0] >= _Y) || (h[1] >= _X)) {
            throw new ArrayIndexOutOfBoundsException();
        }

        return new Integer((h[0] * _X) + h[1]);
    }

    // Convert an Integer to a point
    private int[] i2p(Integer p) {
        return i2p(p.intValue());
    }

    // Convert an int to a point
    private int[] i2p(int p) throws ArrayIndexOutOfBoundsException {
        int[] h = new int[2];

        if (p < 0) {
            throw new ArrayIndexOutOfBoundsException();
        } else {
            h[0] = ((int) p) / _X;
            h[1] = ((int) p) % _X;
        }

        return h;
    }

    // Return true iff we are not at the left or bottom of the map
    private boolean canl(Integer hi) {
        int[] h = i2p(hi);

        return (h[0] > 0) && (h[1] > 0);
    }

    // Return true iff we are not at the right or top of the map
    private boolean canr(Integer hi) {
        int[] h = i2p(hi);

        return (h[0] < (_Y - 1)) && (h[1] < (_X - 1));
    }

    // The hit down-left of this hit
    private Integer hitl(Integer h) throws ArrayIndexOutOfBoundsException {
        if (!canl(h)) {
            throw new ArrayIndexOutOfBoundsException();
        }

        return new Integer(h.intValue() - _X - 1);
    }

    // The hit up-right of this hit
    private Integer hitr(Integer h) throws ArrayIndexOutOfBoundsException {
        if (!canr(h)) {
            throw new ArrayIndexOutOfBoundsException();
        }

        return new Integer(h.intValue() + _X + 1);
    }

    // The leftmost hit in this run
    private Integer leftmost(Integer h) throws ArrayIndexOutOfBoundsException {
        if ((h.intValue() == -1) || !_hits.contains(h)) {
            throw new ArrayIndexOutOfBoundsException();
        }

        Integer h2 = new Integer(h.intValue());

        while (canl(h2) && _hits.contains(hitl(h2))) {
            h2 = hitl(h2);
        }

        return h2;
    }

    // The rightmost hit in this run
    private Integer rightmost(Integer h) throws ArrayIndexOutOfBoundsException {
        if ((h.intValue() == -1) || !_hits.contains(h)) {
            throw new ArrayIndexOutOfBoundsException();
        }

        Integer h2 = new Integer(h.intValue());

        while (canr(h2) && _hits.contains(hitr(h2))) {
            h2 = hitr(h2);
        }

        return h2;
    }

    // The length of the run between two hits, inclusive
    private int runlength(Integer h1, Integer h2)
        throws ArrayIndexOutOfBoundsException {
        if ((h1.intValue() == -1) || !_hits.contains(h1)) {
            throw new ArrayIndexOutOfBoundsException();
        }

        if ((h2.intValue() == -1) || !_hits.contains(h2)) {
            throw new ArrayIndexOutOfBoundsException();
        }

        int hl = h1.intValue();
        int hr = h2.intValue();

        if (((hr - hl) % (_X + 1)) != 0) {
            throw new ArrayIndexOutOfBoundsException();
        }

        return ((hr - hl) / (_X + 1)) + 1;
    }

    public double score(double exponent, double maxHits)
        throws ArrayIndexOutOfBoundsException {
        double score = 0;

        boolean[] xused = new boolean[_X];
        boolean[] yused = new boolean[_Y];

        Iterator iterator = _runs.iterator();
        while (iterator.hasNext()) {
            if (maxHits <= 0) {
                break;
            }
            Run run = (Run)iterator.next();
            double len = run.getLength();
            if (len > maxHits) {
                len = maxHits;
            }
            boolean con = false;
            int[] hp = i2p(run.getPoint());
            for (int i=0; i<len && con!=true; i++) {
                if (xused[hp[1]+i] || yused[hp[0]+i]) {
                    con = true;
                }
            }
            if (con) {
                continue;
            }
            for (int i=0; i<len; i++) {
                xused[hp[1]+i] = true;
                yused[hp[0]+i] = true;
            }
            maxHits -= len;
	    int[] ep = new int[2];
	    ep[0] = hp[0] + (int)len;
	    ep[1] = hp[1] + (int)len;
	    if(runWriter != null) {
		runWriter.print("(" + hp[0] + " " + hp[1] + ", " + ep[0] + " " + ep[1] + ") ");
	    }
            score += Math.pow(len, exponent); 
        }
	
	if(runWriter != null) {
	    runWriter.println();
	}

        //System.err.println("score = " + score);
        return score;
    }
}
