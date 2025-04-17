import { useState } from 'react'
import {
    AreaChart,
    Area,
    CartesianGrid,
    ResponsiveContainer,
    Tooltip,
    XAxis,
    YAxis,
} from 'recharts'

import { SalesGraphTooltip } from './salesgraphtooltip'
import { SalesGraphToggle } from './salesgraphtoggle'

import './salesgraph.styles.css'

export interface SalesGraphData {
    timestamp: string
    total_views: number
    total_cart_adds: number
    total_purchases: number
}

interface SalesGraphProps {
    enableToggles: boolean
    salesData: SalesGraphData[]
}

const SalesGraph: React.FC<SalesGraphProps> = ({
    enableToggles,
    salesData,
}) => {
    const [showViews, setShowViews] = useState(false)
    const [showCarts, setShowCarts] = useState(true)
    const [showPurchases, setShowPurchases] = useState(true)

    const toggleViews = () => {
        if (showViews && !showCarts && !showPurchases) return
        setShowViews((prev) => !prev)
    }

    const toggleCarts = () => {
        if (!showViews && showCarts && !showPurchases) return
        setShowCarts((prev) => !prev)
    }

    const togglePurchases = () => {
        if (!showViews && !showCarts && showPurchases) return
        setShowPurchases((prev) => !prev)
    }

    return (
        <div className="salesgraph">
            <div className="salesgraph__content">
                <ResponsiveContainer>
                    <AreaChart
                        data={salesData}
                        margin={{ top: 10, right: 30, left: 10, bottom: 0 }}
                    >
                        <defs>
                            <linearGradient
                                id="colorViews"
                                x1="0"
                                y1="0"
                                x2="0"
                                y2="1"
                            >
                                <stop
                                    offset="5%"
                                    stopColor="var(--color-accent)"
                                    stopOpacity={0.6}
                                />
                                <stop
                                    offset="95%"
                                    stopColor="var(--color-accent)"
                                    stopOpacity={0.05}
                                />
                            </linearGradient>
                            <linearGradient
                                id="colorCarts"
                                x1="0"
                                y1="0"
                                x2="0"
                                y2="1"
                            >
                                <stop
                                    offset="5%"
                                    stopColor="var(--color-success)"
                                    stopOpacity={0.6}
                                />
                                <stop
                                    offset="95%"
                                    stopColor="var(--color-success)"
                                    stopOpacity={0.05}
                                />
                            </linearGradient>
                            <linearGradient
                                id="colorPurchases"
                                x1="0"
                                y1="0"
                                x2="0"
                                y2="1"
                            >
                                <stop
                                    offset="5%"
                                    stopColor="var(--color-error)"
                                    stopOpacity={0.6}
                                />
                                <stop
                                    offset="95%"
                                    stopColor="var(--color-error)"
                                    stopOpacity={0.05}
                                />
                            </linearGradient>
                        </defs>

                        <CartesianGrid
                            stroke="var(--color-background-light)"
                            vertical={false}
                        />
                        <XAxis dataKey="timestamp" hide />
                        <YAxis hide />
                        <Tooltip content={<SalesGraphTooltip />} />

                        {showViews && (
                            <Area
                                type="monotone"
                                dataKey="total_views"
                                stroke="var(--color-accent)"
                                fill="url(#colorViews)"
                                strokeWidth={2}
                            />
                        )}
                        {showCarts && (
                            <Area
                                type="monotone"
                                dataKey="total_cart_adds"
                                stroke="var(--color-success)"
                                fill="url(#colorCarts)"
                                strokeWidth={2}
                            />
                        )}
                        {showPurchases && (
                            <Area
                                type="monotone"
                                dataKey="total_purchases"
                                stroke="var(--color-error)"
                                fill="url(#colorPurchases)"
                                strokeWidth={2}
                            />
                        )}
                    </AreaChart>
                </ResponsiveContainer>
            </div>
            {enableToggles && (
                <SalesGraphToggle
                    showViews={showViews}
                    showCarts={showCarts}
                    showPurchases={showPurchases}
                    toggleViews={toggleViews}
                    toggleCarts={toggleCarts}
                    togglePurchases={togglePurchases}
                />
            )}
        </div>
    )
}

export default SalesGraph
