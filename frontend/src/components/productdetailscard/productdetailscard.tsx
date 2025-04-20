import {
    BanknotesIcon,
    CreditCardIcon,
    CurrencyDollarIcon,
    EyeIcon,
    StarIcon,
    TagIcon,
} from '@heroicons/react/24/solid'

import { convertValueToString } from '../../components/summarycard/summarycard'
import { isDev } from '../../api/axios'

import './productdetailscard.styles.css'

const SpecItem = ({ Icon, value }: { Icon: any; value: string | number }) => (
    <div className="analytics__product-spec">
        <Icon className="analytics__product-icon" />
        <p className="muted-text">{value}</p>
    </div>
)

const ProductDetailsCard = ({ product, productId }: any) => {
    const specs = [
        {
            icon: TagIcon,
            value:
                product.category === 'Pre-Built PC'
                    ? 'Desktop'
                    : product.category,
        },
        { icon: StarIcon, value: product.average_rating },
        {
            icon: EyeIcon,
            value: convertValueToString('views', product.total_views),
        },
        {
            icon: CurrencyDollarIcon,
            value: convertValueToString('revenue', product.revenue),
        },
        {
            icon: BanknotesIcon,
            value: convertValueToString('cart_adds', product.total_cart_adds),
        },
        {
            icon: CreditCardIcon,
            value: convertValueToString('purchases', product.total_purchases),
        },
    ]

    return (
        <div className="analytics__product-details">
            <img
                src={
                    isDev
                        ? `${import.meta.env.VITE_API_URL}/cdn-assets/product/${productId}.jpg`
                        : `/cdn-assets/product/${productId}.jpg`
                }
                alt={productId + ' Image'}
                className="analytics__product-image"
            />
            <h2>{product.product_name}</h2>
            <div className="analytics__product-specs">
                {specs.map(({ icon, value }, idx) => (
                    <SpecItem key={idx} Icon={icon} value={value} />
                ))}
            </div>
        </div>
    )
}

export default ProductDetailsCard
