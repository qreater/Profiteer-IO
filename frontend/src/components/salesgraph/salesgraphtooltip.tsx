import { TooltipProps } from 'recharts'
import {
    ValueType,
    NameType,
} from 'recharts/types/component/DefaultTooltipContent'

export const SalesGraphTooltip = ({
    active,
    payload,
    label,
}: TooltipProps<ValueType, NameType>) => {
    if (!active || !payload || !payload.length) return null

    const colorMap = {
        total_views: 'var(--color-accent)',
        total_cart_adds: 'var(--color-success)',
        total_purchases: 'var(--color-error)',
    }

    return (
        <div className="salesgraph__tooltip">
            <div className="salesgraph__tooltip-header">
                🕒{' '}
                {new Date(label).toLocaleString(undefined, {
                    month: 'short',
                    day: 'numeric',
                    year: 'numeric',
                    hour: '2-digit',
                    minute: '2-digit',
                })}
            </div>
            {payload.map((entry, index) => (
                <div key={index} className="salesgraph__tooltip-row">
                    <span className="salesgraph__tooltip-label">
                        {entry.name
                            ? entry.name
                                  .toString()
                                  .replace('total_', '')
                                  .replace(/_/g, ' ')
                                  .toUpperCase()
                            : 'UNKNOWN'}
                    </span>
                    <span
                        className="salesgraph__tooltip-value"
                        style={{
                            color:
                                entry.name && entry.name in colorMap
                                    ? colorMap[
                                          entry.name as keyof typeof colorMap
                                      ]
                                    : 'inherit',
                        }}
                    >
                        {entry.value ?? 'N/A'}
                    </span>
                </div>
            ))}
        </div>
    )
}
