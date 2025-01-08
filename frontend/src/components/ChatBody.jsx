import { chats } from "../chat_model";


export default function ChatBody() {
    return <div className="chat-body">
        <div className="message-container">
            <ul className="message-list">
                {chats.map((data)=>{
                    return <li className={`message-tile ${data.sender_id !== 1 ? "chat-right" : ""}`} key={data.id}>{data.message}</li>
                })}
            </ul>
        </div>
                
            </div>
}