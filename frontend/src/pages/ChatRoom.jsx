import ChatScreen from "../components/ChatScreen";
import ChatSideList from "../components/ChatSideList";

export default function ChatRoom() {
    return <div className="main">
        <div className="chat-container">
            <ChatSideList />
            <ChatScreen />
        </div>
    </div>
}