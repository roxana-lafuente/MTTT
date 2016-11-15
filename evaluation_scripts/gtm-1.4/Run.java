//
// Run.java
// $Id: Run.java 2 2006-01-25 03:32:06Z turian $
//
// written by Ryan Green, Joseph P. Turian, I. Dan Melamed, and Luke Shen
// Copyright (c) 2003, New York University
//
// Core routines for creating and sorting runs
//

public class Run implements Comparable {


	private Integer point = null;
	private int length = -1;

	public Run(Integer point, int length) {
		this.point = point;
		this.length = length; 
	}

	public void setPoint(Integer point) {
		this.point = point;
	}

	public void setLength(int length) {
		this.length = length;
	}

	public Integer getPoint() {
		return point;
	}

	public int getLength() {
		return length;
	}
 
	public int compareTo(Object run) {
		if (this.length > ((Run)run).getLength() || (this.length == ((Run)run).getLength() && this.point.intValue() > ((Run)run).getPoint().intValue() )) {
			return -1;
		} else if (this.length == ((Run)run).getLength() && this.point.intValue() == ((Run)run).getPoint().intValue()) {
			System.err.println("You should not be comparing equal runs. Exiting ...");
			System.exit(-1);
                        return 0;
		} else {
			return 1;
		}
	}

        public String toString() {
                StringBuffer buffer = new StringBuffer();
                buffer.append("Point of the run is: "+point);
                buffer.append("\tLength of the run is: "+length);
                return buffer.toString();
        }
}
