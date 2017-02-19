/*
 * Created by SharpDevelop.
 * User: Eslam
 * Date: Sunday 19 02 2017
 * Time: 2:28 PM
 * 
 * To change this template use Tools | Options | Coding | Edit Standard Headers.
 */
using System;
using WComp.Beans;

namespace WComp.Beans
{
	[Bean(Category="Custom")]
	public class GPSBean
	{
		public delegate void sendAlert(string alertMessage);
		public event sendAlert AlertGPS;
		
		public void AnalyseCoordinates(string gps) {
			if(AlertGPS != null)
				AlertGPS("Location;You can see the cane's location by visiting the following url: https://www.google.fr/maps/@" + gps + ",20z?hl=en");
		}
	}
}
