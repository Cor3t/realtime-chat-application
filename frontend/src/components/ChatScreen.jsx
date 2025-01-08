import ChatBody from "./ChatBody";
import ChatFooter from "./ChatFooter";
import ChatHeader from "./ChatHeader";

export default function ChatScreen() {
    return <div className="chat-screen">
        <ChatHeader title="Uncle Niyi"/>
        <ChatBody />
        <ChatFooter />
        
    </div>
}