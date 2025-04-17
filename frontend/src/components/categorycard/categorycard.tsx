import {
    ArrowTrendingDownIcon,
    ArrowTrendingUpIcon,
    BanknotesIcon,
} from '@heroicons/react/24/solid'
import { convertValueToString } from '../summarycard/summarycard'

import './categorycard.styles.css'

interface CategoryCardProps {
    name: string
    revenue: number
    has_increased: boolean
}

const CategoryCard: React.FC<CategoryCardProps> = ({
    name,
    revenue,
    has_increased,
}) => {
    return (
        <div className="categorycard">
            <div className="categorycard__wrapper">
                <div className="categorycard__content">
                    <BanknotesIcon className="categorycard__icon text-accent" />
                    <h1
                        className={`focus-text ${has_increased ? 'text-success' : 'text-error'}`}
                    >
                        {convertValueToString('revenue', revenue)}
                    </h1>
                </div>
                <div className="categorycard__content">
                    <h2>{name}</h2>
                </div>
            </div>
            <div className="categorycard__content">
                {has_increased ? (
                    <ArrowTrendingUpIcon className="categorycard__icon text-success" />
                ) : (
                    <ArrowTrendingDownIcon className="categorycard__icon text-error" />
                )}
            </div>
        </div>
    )
}

export default CategoryCard
