import Navbar from '../navbar/navbar'

import './layout.styles.css'

interface LayoutProps {
    children: React.ReactNode
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
    return (
        <div className="layout">
            <Navbar />
            <div className="layout__children">{children}</div>
        </div>
    )
}

export default Layout
