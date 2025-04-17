import { useEffect, useState } from 'react'
import { useDashboardData } from '../../api/hooks/dashboard'
import CategoryCard from '../../components/categorycard/categorycard'
import HotProductCard from '../../components/hotproductcard/hotproductcard'
import Loading from '../../components/loading/loading'
import SalesGraph from '../../components/salesgraph/salesgraph'
import SummaryCard from '../../components/summarycard/summarycard'

import './dashboard.styles.css'

const Dashboard: React.FC = () => {
    const { summary, graph, category, hotProducts, loading, error } =
        useDashboardData()

    const [minDelayDone, setMinDelayDone] = useState(false)

    const dashboardData = summary
        .map((entry) => [
            {
                title: 'Revenue',
                focusValue: entry.revenue,
                focusPercentage: entry.revenue_change_pct,
            },
            {
                title: 'Items Sold',
                focusValue: entry.items,
                focusPercentage: entry.items_change_pct,
            },
            {
                title: 'Conversion Rate',
                focusValue: `${entry.conversion_rate}%`,
                focusPercentage: entry.conversion_rate_change_pct,
            },
            {
                title: 'Top Category',
                focusValue: entry.top_category,
                focusPercentage: null,
            },
        ])
        .flat()

    useEffect(() => {
        const timer = setTimeout(() => {
            setMinDelayDone(true)
        }, 3000)
        return () => clearTimeout(timer)
    }, [])

    if (loading || !minDelayDone) {
        return <Loading />
    }

    if (error) return <p>Error: {error}</p>

    return (
        <div className="dashboard">
            <div className="dashboard__summary">
                <h1>Summary (24 Hr)</h1>
                <div className="dashboard__summary__content">
                    {dashboardData.map((data, index) => (
                        <SummaryCard
                            key={index}
                            title={data.title}
                            focusValue={data.focusValue}
                            focusPercentage={data.focusPercentage}
                        />
                    ))}
                </div>
            </div>
            <div className="dashboard__graph">
                <h1>Sales Data</h1>
                <SalesGraph enableToggles={true} salesData={graph} />
            </div>
            <div className="dashboard__categories">
                <h1>Categories</h1>
                <div className="dashboard__categories__content">
                    {category.map((category, index) => (
                        <CategoryCard
                            key={index}
                            name={category.name}
                            revenue={category.revenue}
                            has_increased={category.has_increased}
                        />
                    ))}
                </div>
            </div>
            <div className="dashboard__products">
                <h1>Hot Products</h1>
                <div className="dashboard__products__content">
                    {hotProducts.map((product, _) => (
                        <HotProductCard
                            key={product.id}
                            name={product.name}
                            revenue={product.revenue}
                            category={product.category}
                        />
                    ))}
                </div>
            </div>
        </div>
    )
}

export default Dashboard
