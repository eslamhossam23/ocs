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
	/// <summary>
	/// This is a sample bean, which has an integer evented property and a method.
	/// 
	/// Notes: for beans creating threads, the IThreadCreator interface should be implemented,
	/// 	providing a cleanup method should be implemented and named `Stop()'.
	/// For proxy beans, the IProxyBean interface should  be implemented,
	/// 	providing the IsConnected property, allowing the connection status to be drawn in
	/// 	the AddIn's graphical designer.
	/// 
	/// Several classes can be defined or used by a Bean, but only the class with the
	/// [Bean] attribute will be available in WComp. Its ports will be all public methods,
	/// events and properties definied in that class.
	/// </summary>
	[Bean(Category="Custom")]
	public class StepBean
	{

		private int threshold;

		public int Threshold {
			get { return threshold; }
			set {
				threshold = value;
			}
		}

		public delegate void sendAlert(string alertMessage);
		public event sendAlert AlertSteps;
		
		public delegate void stopCounting();
		public event stopCounting StopCounting;
		
		
		public void AnalyseSteps(string steps) {
			if(Int32.Parse(steps) > threshold){
				if (AlertSteps != null)
					AlertSteps("Alert Steps;You have exceeded the number of steps you had to do today at: " + steps);
				if(StopCounting != null)
					StopCounting();
			}
			
		}
	}
}
