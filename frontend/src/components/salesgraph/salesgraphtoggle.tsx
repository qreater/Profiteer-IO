import {
    CreditCardIcon,
    EyeIcon,
    ShoppingCartIcon,
} from '@heroicons/react/24/solid'

interface ToggleProps {
    showViews: boolean
    showCarts: boolean
    showPurchases: boolean
    toggleViews: () => void
    toggleCarts: () => void
    togglePurchases: () => void
}

export const SalesGraphToggle = ({
    showViews,
    showCarts,
    showPurchases,
    toggleViews,
    toggleCarts,
    togglePurchases,
}: ToggleProps) => {
    return (
        <div className="salesgraph__toggles">
            <div
                className={`salesgraph__toggle ${showViews ? 'salesgraph__toggle--active' : ''}`}
                onClick={toggleViews}
            >
                <EyeIcon className="salesgraph__icon" />
            </div>
            <div
                className={`salesgraph__toggle ${showCarts ? 'salesgraph__toggle--active' : ''}`}
                onClick={toggleCarts}
            >
                <ShoppingCartIcon className="salesgraph__icon" />
            </div>
            <div
                className={`salesgraph__toggle ${showPurchases ? 'salesgraph__toggle--active' : ''}`}
                onClick={togglePurchases}
            >
                <CreditCardIcon className="salesgraph__icon" />
            </div>
        </div>
    )
}
