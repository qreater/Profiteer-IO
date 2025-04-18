import Slider from 'react-slick'
import { CatalogProduct } from '../../api/hooks/catalog'
import ProductCard from '../productcard/productcard'
import {
    ChevronDoubleLeftIcon,
    ChevronDoubleRightIcon,
} from '@heroicons/react/24/solid'

import 'slick-carousel/slick/slick.css'
import 'slick-carousel/slick/slick-theme.css'
import './productcarousel.styles.css'

interface ProductCarouselProps {
    products: CatalogProduct[]
}

interface CustomArrowProps {
    className?: string
    style?: React.CSSProperties
    onClick?: React.MouseEventHandler<HTMLDivElement>
}

export const PrevArrow: React.FC<CustomArrowProps> = ({
    onClick,
    className = '',
    style: _style,
}) => {
    const isDisabled = className.includes('slick-disabled')

    return (
        <div
            className={`custom-arrow left ${isDisabled ? 'disabled' : ''}`}
            onClick={onClick}
        >
            <ChevronDoubleLeftIcon className="arrow-icon" />
        </div>
    )
}

export const NextArrow: React.FC<CustomArrowProps> = ({
    onClick,
    className = '',
    style: _style,
}) => {
    const isDisabled = className.includes('slick-disabled')

    return (
        <div
            className={`custom-arrow right ${isDisabled ? 'disabled' : ''}`}
            onClick={onClick}
        >
            <ChevronDoubleRightIcon className="arrow-icon" />
        </div>
    )
}

const ProductCarousel: React.FC<ProductCarouselProps> = ({ products }) => {
    const settings = {
        dots: false,
        focusOnSelect: false,
        infinite: false,
        speed: 500,
        slidesToShow: 3,
        slidesToScroll: 1,
        nextArrow: <NextArrow />,
        prevArrow: <PrevArrow />,
        arrows: true,
        responsive: [
            {
                breakpoint: 1024,
                settings: {
                    slidesToShow: 2,
                },
            },
            {
                breakpoint: 640,
                settings: {
                    slidesToShow: 1,
                },
            },
        ],
    }

    return (
        <div className="productcarousel">
            <Slider {...settings}>
                {products.map((product) => (
                    <div key={product.product_id}>
                        <ProductCard {...product} />
                    </div>
                ))}
            </Slider>
        </div>
    )
}

export default ProductCarousel
