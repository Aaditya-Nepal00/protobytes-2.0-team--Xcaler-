import { useState, useEffect, useRef } from 'react'
import lawsService from '../../services/laws.service'

interface Message {
    id: string
    text: string
    sender: 'bot' | 'user'
}

export default function LawBot() {
    const [isOpen, setIsOpen] = useState(false)
    const [messages, setMessages] = useState<Message[]>([
        { id: '1', text: 'Namaste! I am the Sachet Law Bot. You can ask me about any crime, law, or right in Nepal.', sender: 'bot' }
    ])
    const [laws, setLaws] = useState<any[]>([])
    const [isTyping, setIsTyping] = useState(false)
    const [input, setInput] = useState('')
    const chatBodyRef = useRef<HTMLDivElement>(null)

    useEffect(() => {
        lawsService.getLaws({ per_page: 5 })
            .then(res => setLaws(res.laws))
            .catch(() => { })
    }, [])

    useEffect(() => {
        if (chatBodyRef.current) {
            chatBodyRef.current.scrollTop = chatBodyRef.current.scrollHeight
        }
    }, [messages])

    const addMessage = (text: string, sender: 'bot' | 'user') => {
        setMessages(prev => [...prev, { id: Date.now().toString(), text, sender }])
    }

    const handleSend = async (e?: React.FormEvent) => {
        if (e) e.preventDefault()
        if (!input.trim() || isTyping) return

        const userMsg = input.trim()
        setInput('')
        addMessage(userMsg, 'user')
        setIsTyping(true)

        // Mock AI Logic
        setTimeout(() => {
            let response = "I'm still learning about that specific topic. Try asking about 'theft', 'cybercrime', 'RTI', or 'corruption'."

            const lowerMsg = userMsg.toLowerCase()
            if (lowerMsg.includes('theft') || lowerMsg.includes('chori')) {
                response = "In Nepal, theft (Muluki Aparadh Sanhita) carries a punishment of up to 3 years in prison and a fine of Rs 30,000. For robbery, it's 5 to 10 years. Always report such incidents to 100 immediately."
            } else if (lowerMsg.includes('cyber') || lowerMsg.includes('facebook') || lowerMsg.includes('hacking')) {
                response = "Cybercrime is handled under the Electronic Transactions Act. Offenses like social media harassment or hacking can lead to 5 years in jail or a Rs 2 lakh fine."
            } else if (lowerMsg.includes('rti') || lowerMsg.includes('information')) {
                response = "The Right to Information Act allows you to request information from any public body. They MUST provide it within 15 days, or you can appeal to the National Information Commission."
            } else if (lowerMsg.includes('corruption') || lowerMsg.includes('bribe')) {
                response = "Taking or giving bribes is a crime under the Anti-Corruption Act. You can report this anonymously on our portal, and the CIAA will investigate."
            } else if (lowerMsg.includes('hello') || lowerMsg.includes('hi') || lowerMsg.includes('namaste')) {
                response = "Namaste! How can I help you today? I can simplify complex Nepali laws for you."
            }

            setIsTyping(false)
            addMessage(response, 'bot')
        }, 1500)
    }

    const handleSelectLaw = async (law: any) => {
        addMessage(`Simplify the ${law.title}.`, 'user')
        setIsTyping(true)

        try {
            const fullLaw = await lawsService.getLawById(law.id)
            const content = fullLaw.simplified || fullLaw.content || "I don't have simplified details for this law yet."
            const lines = content.split(/[.!?]/).filter((l: string) => l.trim().length > 0)

            setTimeout(() => {
                setIsTyping(false)
                addMessage(`The ${law.title} simplified:`, 'bot')
                lines.forEach((line: string, index: number) => {
                    setTimeout(() => {
                        addMessage(line.trim() + '.', 'bot')
                    }, (index + 1) * 1200)
                });
            }, 800)
        } catch (err) {
            setIsTyping(false)
            addMessage("I couldn't fetch that law right now. Please try again.", 'bot')
        }
    }

    return (
        <>
            <button className="chatbot-float" onClick={() => setIsOpen(!isOpen)}>
                {isOpen ? <span style={{ fontSize: '1.5rem' }}>✕</span> : "💬"}
            </button>

            {isOpen && (
                <div className="chatbot-window">
                    <div className="chat-header">
                        <div style={{ width: 40, height: 40, background: 'rgba(255,255,255,0.2)', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>⚖️</div>
                        <div style={{ marginLeft: 12 }}>
                            <div style={{ fontWeight: 800 }}>Sachet Law Bot</div>
                            <div style={{ fontSize: '0.7rem', opacity: 0.8 }}>Online • AI Legal Assistant</div>
                        </div>
                    </div>

                    <div className="chat-body" ref={chatBodyRef}>
                        {messages.map(m => (
                            <div key={m.id} className={`msg msg-${m.sender}`}>
                                {m.text}
                            </div>
                        ))}
                        {isTyping && <div className="msg msg-bot">... typing</div>}
                    </div>

                    <div className="chat-footer" style={{ padding: '12px', borderTop: '1px solid var(--border-color)' }}>
                        <div style={{ display: 'flex', gap: 6, marginBottom: 10, overflowX: 'auto', paddingBottom: 4 }}>
                            {laws.map(l => (
                                <button key={l.id} className="btn-chip" onClick={() => handleSelectLaw(l)}>
                                    {l.title.split(' ')[0]}
                                </button>
                            ))}
                        </div>
                        <form onSubmit={handleSend} style={{ display: 'flex', gap: 8 }}>
                            <input
                                type="text"
                                className="input"
                                placeholder="Type a crime or law..."
                                value={input}
                                onChange={e => setInput(e.target.value)}
                                style={{ borderRadius: '20px', padding: '10px 15px', height: '40px' }}
                            />
                            <button type="submit" className="btn btn-primary" style={{ borderRadius: '50%', width: 40, height: 40, padding: 0 }}>
                                ➔
                            </button>
                        </form>
                    </div>
                </div>
            )}
            <style>{`
                .btn-chip {
                    background: var(--bg-body);
                    border: 1px solid var(--border-color);
                    padding: 4px 10px;
                    border-radius: 12px;
                    font-size: 0.75rem;
                    white-space: nowrap;
                    color: var(--primary);
                    cursor: pointer;
                    transition: all 0.2s;
                }
                .btn-chip:hover { background: var(--primary); color: white; }
            `}</style>
        </>
    )
}
