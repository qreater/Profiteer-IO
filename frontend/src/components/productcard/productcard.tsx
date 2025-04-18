import { BanknotesIcon, StarIcon } from '@heroicons/react/24/solid'
import { CatalogProduct } from '../../api/hooks/catalog'

import { convertValueToString } from '../summarycard/summarycard'

import './productcard.styles.css'

const ProductCard: React.FC<CatalogProduct> = ({
    product_id,
    product_name,
    product_image: _,
    average_rating,
    revenue,
}) => {
    return (
        <div className="productcard">
            <img
                src={
                    import.meta.env.VITE_API_URL +
                    '/cdn-assets/product/' +
                    product_id +
                    '.jpg'
                }
                alt={product_name}
                className="productcard__image"
            />
            <div className="productcard__header">
                <div className="productcard__revenue">
                    <BanknotesIcon className="productcard__revenue__icon text-accent" />
                    <h1 className="focus-text text-accent">
                        {convertValueToString('revenue', revenue)}
                    </h1>
                </div>
                <h2>{product_name}</h2>
            </div>
            <div className="productcard__footer">
                <h2>{product_id}</h2>
                <div className="productcard__rating">
                    <StarIcon
                        className={`productcard__rating__icon ${average_rating > 3.5 ? 'text-success' : 'text-error'}`}
                    />
                    <h2
                        className={`${average_rating > 3.5 ? 'text-success' : 'text-error'}`}
                    >
                        {average_rating}
                    </h2>
                </div>
            </div>
        </div>
    )
}

export default ProductCard
