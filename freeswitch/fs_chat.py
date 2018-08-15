from .ESL import ESLconnection, ESLevent

def send_chat(user, ip, port, msg, frUser="guson"):
    con = ESLconnection("127.0.0.1", "8021", "ClueCon")
    
    event = ESLevent("CUSTOM", "SMS::SEND_MESSAGE")
    event.addHeader("sip_profile", "internal")
    event.addHeader("type", "text/plain")
    event.addHeader("dest_proto", "sip")

    event.addHeader("from", frUser)

    event.addHeader("to", user)
    event.addHeader("to_sip_ip", ip)
    event.addHeader("to_sip_port", port)
    event.addBody(msg)

    con.sendEvent(event)