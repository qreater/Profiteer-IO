import React, { useCallback } from 'react'
import { useLocation, useNavigate } from 'react-router'

import './navbar.styles.css'
import {
    HomeIcon,
    ArchiveBoxIcon,
    ChartBarIcon,
} from '@heroicons/react/24/solid'

const navbarItems = [
    {
        name: 'Dashboard',
        path: '/',
        icon: HomeIcon,
    },
    {
        name: 'Catalog',
        path: '/catalog',
        icon: ArchiveBoxIcon,
    },
    {
        name: 'Prediction',
        path: '/prediction',
        icon: ChartBarIcon,
    },
]

const Navbar: React.FC = () => {
    const location = useLocation()
    const navigate = useNavigate()

    const handleNavigation = useCallback(
        (path: string) => {
            if (location.pathname === path) return
            navigate(path)
        },
        [location.pathname, navigate],
    )

    return (
        <div className="navbar">
            <div className="navbar__items">
                {navbarItems.map((item) => (
                    <div
                        key={item.path}
                        className={`navbar__item ${location.pathname === item.path ? 'navbar__item--active' : ''}`}
                        onClick={() => handleNavigation(item.path)}
                    >
                        <item.icon className="navbar__icon" />
                    </div>
                ))}
            </div>
        </div>
    )
}

export default Navbar
