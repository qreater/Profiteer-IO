import './summarycard.styles.css'

interface SummaryCardProps {
    title: string
    focusValue: string | number
    focusPercentage: number | null
}

export const convertValueToString = (
    title: string,
    value: number | string,
): string => {
    if (typeof value === 'string') return value
    if (value === null || value === undefined) return ''

    const valueEstimate = value
    const isNegative = valueEstimate < 0
    const absValue = Math.abs(valueEstimate)

    let formatted = ''
    if (absValue >= 1_000_000_000) {
        formatted = `${(absValue / 1_000_000_000).toFixed(1)}B`
    } else if (absValue >= 1_000_000) {
        formatted = `${(absValue / 1_000_000).toFixed(1)}M`
    } else if (absValue >= 1_000) {
        formatted = `${(absValue / 1_000).toFixed(1)}K`
    } else {
        formatted = absValue.toFixed(absValue % 1 === 0 ? 0 : 1)
    }

    if (isNegative) {
        formatted = `-${formatted}`
    }

    if (title.toLowerCase() === 'revenue') {
        return `$${formatted}`
    }

    return formatted
}

const getFocusPercentageBadge = (percentage: number): string => {
    return percentage >= 0
        ? 'summarycard__badge--success'
        : 'summarycard__badge--error'
}

const FocusBadge: React.FC<{ percentage: number }> = ({ percentage }) => (
    <div
        className={`summarycard__badge ${getFocusPercentageBadge(percentage)}`}
    >
        <h2>
            {percentage > 0 ? '+' : ''}
            {percentage.toFixed(1)}%
        </h2>
    </div>
)

const SummaryCard: React.FC<SummaryCardProps> = ({
    title,
    focusValue,
    focusPercentage,
}) => {
    return (
        <div className="summarycard">
            <div className="summarycard__content">
                <h1
                    className={`focus-text ${focusPercentage !== null ? (focusPercentage > 0 ? 'text-success' : 'text-error') : 'text-accent'}`}
                >
                    {convertValueToString(title, focusValue)}
                </h1>
            </div>
            <div className="summarycard__content">
                <h2>{title}</h2>
                {focusPercentage !== null && (
                    <FocusBadge percentage={focusPercentage} />
                )}
            </div>
        </div>
    )
}

export default SummaryCard
