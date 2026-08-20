import os
import smtplib
from email.message import EmailMessage

def send_result_email(to_email: str, result_title: str, result_content: str, attachment_path: str = None, booking_link: str = "#", already_booked: bool = False, is_qualified: bool = True, selected_songs: list = None) -> bool:
    """
    Sends a formatted HTML email containing the lead's result.
    """
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com").strip()
    port_str = os.getenv("SMTP_PORT", "465").strip()
    smtp_port = int(port_str) if port_str else 465
    smtp_username = os.getenv("SMTP_USERNAME", "").strip()
    smtp_password = os.getenv("SMTP_PASSWORD", "").strip()

    if not smtp_username or not smtp_password:
        print("SMTP Credentials not configured. Skipping email send.")
        return False

    msg = EmailMessage()
    msg['Subject'] = f"Your Guitar Playing Profile: {result_title}"
    msg['From'] = smtp_username
    msg['To'] = to_email

    # Format the content into HTML
    # Replacing newlines with <br> and bullet points with styled text
    formatted_content = result_content.replace("\n", "<br>")
    
    songs_html = ""
    if selected_songs and len(selected_songs) > 0:
        songs_list = "".join([f"<li>{song}</li>" for song in selected_songs])
        songs_html = f"""
        <h2 style="color: #006b43;">🎸 Your 5-Song Guitar Goal</h2>
        <ul style="font-size: 16px; margin-bottom: 20px;">
          {songs_list}
        </ul>
        """
    
    if already_booked:
        cta_html = f"""
        <div style="background-color: #f4fdf8; padding: 25px; border-radius: 8px; text-align: center; border: 1px solid #e0f2e9;">
          <h3 style="color: #006b43; margin-top: 0; margin-bottom: 15px; font-size: 20px;">You've already booked your 100% Free Consultation</h3>
          <p style="font-size: 16px; color: #333; margin-bottom: 25px;">
            Missed booking?
          </p>
          <p style="margin-bottom: 20px;">
            <a href="{booking_link}" style="display: inline-block; padding: 12px 25px; background-color: #006b43; color: white; text-decoration: none; border-radius: 5px; font-weight: bold; font-size: 16px;">Contact Support</a>
          </p>
        </div>
        """
    else:
        cta_html = f"""
        <div style="background-color: #f4fdf8; padding: 25px; border-radius: 8px; text-align: center; border: 1px solid #e0f2e9;">
          <h3 style="color: #006b43; margin-top: 0; margin-bottom: 15px; font-size: 20px;">100% Free 1:1 Consultation</h3>
          <p style="font-size: 16px; color: #333; margin-bottom: 25px;">
            Want to understand your roadmap better? We help you understand with a 100% free 1:1 consultation from top mentors.
          </p>
          <p style="margin-bottom: 20px;">
            <a href="{booking_link}" style="display: inline-block; padding: 12px 25px; background-color: #006b43; color: white; text-decoration: none; border-radius: 5px; font-weight: bold; font-size: 16px;">Book Free Strategy Session</a>
          </p>
          <p style="font-size: 12px; color: #666; margin-bottom: 0;">
            If the button above does not work, copy and paste this link into your browser:<br><a href="{booking_link}" style="color: #006b43;">{booking_link}</a>
          </p>
        </div>
        """

    html_content = f"""
    <html>
      <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
        <div style="text-align: center; margin-bottom: 30px;">
          <img src="cid:logo" alt="Logo" style="max-height: 80px;" />
        </div>
        <h2 style="color: #006b43;">{result_title}</h2>
        <p>{formatted_content}</p>
        {songs_html}
        <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
        {cta_html}
      </body>
    </html>
    """
    msg.set_content("Please enable HTML to view this email.")
    msg.add_alternative(html_content, subtype='html')

    # Add inline logo
    logo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'assets', 'logo.png')
    if os.path.exists(logo_path):
        with open(logo_path, 'rb') as img:
            try:
                msg.get_payload()[1].add_related(img.read(), maintype='image', subtype='png', cid='<logo>')
            except Exception as e:
                print(f"Could not attach logo: {e}")

    # Add attachment if provided
    if attachment_path and os.path.exists(attachment_path):
        with open(attachment_path, 'rb') as f:
            pdf_data = f.read()
        msg.add_attachment(pdf_data, maintype='application', subtype='pdf', filename=os.path.basename(attachment_path))

    try:
        # Port 465 is for SMTP_SSL
        if smtp_port == 465:
            with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
                server.login(smtp_username, smtp_password)
                server.send_message(msg)
        else:
            # Port 587 is for TLS
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_username, smtp_password)
                server.send_message(msg)
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

def send_booking_confirmation_email(to_email: str, lead_name: str, time_slot: str, meet_link: str) -> bool:
    """
    Sends a formatted HTML email confirming the strategy call booking.
    """
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com").strip()
    port_str = os.getenv("SMTP_PORT", "465").strip()
    smtp_port = int(port_str) if port_str else 465
    smtp_username = os.getenv("SMTP_USERNAME", "").strip()
    smtp_password = os.getenv("SMTP_PASSWORD", "").strip()

    if not smtp_username or not smtp_password:
        print("SMTP Credentials not configured. Skipping booking email send.")
        return False

    msg = EmailMessage()
    msg['Subject'] = "Booking Confirmed: Your Guitar Strategy Call"
    msg['From'] = smtp_username
    msg['To'] = to_email

    html_content = f"""
    <html>
      <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
        <div style="text-align: center; margin-bottom: 30px;">
          <img src="cid:logo" alt="Logo" style="max-height: 80px;" />
        </div>
        <h2 style="color: #006b43;">Booking Confirmed!</h2>
        <p>Hi {lead_name},</p>
        <p>Your Strategy Call is confirmed for <strong>{time_slot}</strong>.</p>
        <p>Please use the following Google Meet link to join the call at the scheduled time:</p>
        <p><a href="{meet_link}" style="display: inline-block; padding: 10px 20px; background-color: #006b43; color: white; text-decoration: none; border-radius: 5px; font-weight: bold;">Join Strategy Call</a></p>
        <p>If the button above does not work, copy and paste this link into your browser:<br><a href="{meet_link}" style="color: #006b43;">{meet_link}</a></p>
        <p>If you have any questions or need to reschedule, please reply directly to this email.</p>
        <p>We look forward to speaking with you!</p>
        <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
      </body>
    </html>
    """
    msg.set_content("Please enable HTML to view this email.")
    msg.add_alternative(html_content, subtype='html')

    # Add inline logo
    logo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'assets', 'logo.png')
    if os.path.exists(logo_path):
        with open(logo_path, 'rb') as img:
            try:
                msg.get_payload()[1].add_related(img.read(), maintype='image', subtype='png', cid='<logo>')
            except Exception as e:
                print(f"Could not attach logo: {e}")

    try:
        if smtp_port == 465:
            with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
                server.login(smtp_username, smtp_password)
                server.send_message(msg)
        else:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_username, smtp_password)
                server.send_message(msg)
        return True
    except Exception as e:
        print(f"Failed to send booking email: {{e}}")
        return False
