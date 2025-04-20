import React from 'react'
import './priceslider.styles.css'

type PriceSliderProps = {
    basePrice: number
    value: number
    onChange: (value: number) => void
}

const PriceSlider: React.FC<PriceSliderProps> = ({
    basePrice,
    value,
    onChange,
}) => {
    const min = Math.round(basePrice * 0.9)
    const max = Math.round(basePrice * 1.1)

    return (
        <div className="price-slider">
            <p className="price-slider__label">Set Price</p>
            <input
                type="range"
                className="price-slider__input"
                min={min}
                max={max}
                step={1}
                value={value}
                onChange={(e) => onChange(Number(e.target.value))}
            />
            <div className="price-slider__range-labels">
                <div className="price-slider__range-labels__container">
                    <p className="price-slider__label price-slider__label--min">
                        min
                    </p>
                    <p className="price-slider__label">${min}</p>
                </div>
                <div className="price-slider__range-labels__container">
                    <p className="price-slider__label price-slider__label--max">
                        max
                    </p>
                    <p className="price-slider__label">${max}</p>
                </div>
            </div>
        </div>
    )
}

export default PriceSlider
