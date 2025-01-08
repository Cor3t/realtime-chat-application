export default function ChatListTile({title, content}) {
    return <li className="chat-list-tile">
        <p>{title}</p>
        <span>{content}</span>
    </li>
}