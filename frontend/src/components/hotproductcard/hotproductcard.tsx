import { TagIcon } from '@heroicons/react/24/solid'
import { convertValueToString } from '../summarycard/summarycard'
import './hotproductcard.styles.css'

interface HotProductCardProps {
    name: string
    revenue: number
    category: string
}

const HotProductCard: React.FC<HotProductCardProps> = ({
    name,
    revenue,
    category,
}) => {
    return (
        <div className="hotproductcard">
            <div className="hotproductcard__wrapper">
                <div className="hotproductcard__content">
                    <h2>{name}</h2>
                    <div className="hotproductcard__badge">
                        <TagIcon className="hotproductcard__icon text-accent" />
                        <p>{category}</p>
                    </div>
                </div>
                <div className="hotproductcard__content">
                    <h1 className="focus-text text-accent">
                        {convertValueToString('revenue', revenue)}
                    </h1>
                </div>
            </div>
        </div>
    )
}

export default HotProductCard
