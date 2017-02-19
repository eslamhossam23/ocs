/*
 * Created by SharpDevelop.
 * User: Havoc
 * Date: Friday-10-02-2017
 * Time: 12:49 PM
 * 
 * To change this template use Tools | Options | Coding | Edit Standard Headers.
 */
using System;
using System.Net;
using System.Net.Mail;
using WComp.Beans;

namespace WComp.Beans
{
	[Bean(Category="Custom")]
	public class MailBean
	{
		private string to = "eslamhossam23@gmail.com";
		private string from = "canneintelligente@hotmail.com";
		private string password = "canneocs1";
		private string[] messageSeparator = {";"};
		
		public delegate void Sent(string s);
		public event Sent Alert;
		
		public SmtpClient client = new SmtpClient("smtp-mail.outlook.com");
		

		public string To {
			get { return to; }
			set {
				to = value;
			}
		}
		
		public string From {
			get { return from; }
			set {
				from = value;
			}
		}
		
		public string Password {
			get { return password; }
			set {
				password = value;
			}
		}
		
		public string Separator {
			get { return messageSeparator[0]; }
			set {
				messageSeparator[0] = value;
			}
		}
		
		public void SendMail(string s){
			client.UseDefaultCredentials = false;
			client.DeliveryMethod = SmtpDeliveryMethod.Network;
			client.Port = 587;
			client.EnableSsl = true;
			client.Credentials = new NetworkCredential(from,password);
			string[] subjectBody = s.Split(messageSeparator, StringSplitOptions.RemoveEmptyEntries);
			MailMessage message = new MailMessage(
	   		from,
	   		to,
	   		subjectBody[0],
	   		subjectBody[1]);
    		try {
	  			client.Send(message);
	  		if(Alert != null)
				Alert("Mail sent successfully.");
			}
			catch (Exception ex) {
				if(Alert != null)
					Alert(ex.ToString());
			}
		}
		
}
}
