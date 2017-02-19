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
	public class HeartBeatBean
	{
		
		private int threshold;

		public int Threshold {
			get { return threshold; }
			set {
				threshold = value;
			}
		}

		public delegate void sendAlert(string alertMessage);
		public event sendAlert AlertHeartBeat;
		
		public void AnalyseHeartBeat(string heartbeat) {
			if(Int32.Parse(heartbeat) > threshold){
				if (AlertHeartBeat != null)
					AlertHeartBeat("Alert HeartBeat;Your heartbeat is too high at: " + heartbeat + ". You should get some rest.");
			}
		}
	}
}
