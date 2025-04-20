import React, { useState, useRef, useEffect, useLayoutEffect } from 'react'
import './dropdown.styles.css'

interface DropdownProps {
    values: string[]
    selectedValue?: string
    defaultText?: string
    onSelect: (value: string) => void
}

const Dropdown: React.FC<DropdownProps> = ({
    values,
    selectedValue,
    defaultText = 'Select...',
    onSelect,
}) => {
    const [isOpen, setIsOpen] = useState(false)
    const [openUpward, setOpenUpward] = useState(false)
    const [maxHeight, setMaxHeight] = useState<number>(300)

    const dropdownRef = useRef<HTMLDivElement>(null)
    const listRef = useRef<HTMLUListElement>(null)

    const toggleDropdown = () => setIsOpen((prev) => !prev)

    const handleSelect = (value: string) => {
        onSelect(value)
        setIsOpen(false)
    }

    useEffect(() => {
        const handleClickOutside = (event: MouseEvent) => {
            if (
                dropdownRef.current &&
                !dropdownRef.current.contains(event.target as Node)
            ) {
                setIsOpen(false)
            }
        }
        document.addEventListener('mousedown', handleClickOutside)
        return () =>
            document.removeEventListener('mousedown', handleClickOutside)
    }, [])

    useLayoutEffect(() => {
        if (isOpen && dropdownRef.current) {
            const rect = dropdownRef.current.getBoundingClientRect()
            const viewportHeight = window.innerHeight

            const spaceBelow = viewportHeight - rect.bottom
            const spaceAbove = rect.top

            const requiredHeight = Math.min(190, spaceBelow - 20)

            if (spaceBelow < 170 && spaceAbove > spaceBelow) {
                setOpenUpward(true)
                setMaxHeight(Math.min(190, spaceAbove - 20))
            } else {
                setOpenUpward(false)
                setMaxHeight(requiredHeight)
            }
        }
    }, [isOpen])

    return (
        <div className="dropdown" ref={dropdownRef}>
            <div className="dropdown__select" onClick={toggleDropdown}>
                {selectedValue || defaultText}
                <span
                    className={`dropdown__arrow ${isOpen ? 'dropdown__arrow--open' : ''}`}
                />
            </div>

            {isOpen && (
                <ul
                    ref={listRef}
                    className={`dropdown__list ${
                        openUpward
                            ? 'dropdown__list--top'
                            : 'dropdown__list--bottom'
                    }`}
                    style={{ maxHeight: `${maxHeight}px` }}
                >
                    {values.map((value) => (
                        <li
                            key={value}
                            className="dropdown__option"
                            onClick={() => handleSelect(value)}
                        >
                            {value}
                        </li>
                    ))}
                </ul>
            )}
        </div>
    )
}

export default Dropdown
