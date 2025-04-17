import { useState, useEffect } from 'react'
import { isAxiosError } from 'axios'
import axios from '../axios'

type SummaryEntry = {
    revenue: number
    revenue_change_pct: number
    items: number
    items_change_pct: number
    conversion_rate: number
    conversion_rate_change_pct: number
    top_category: string
}

type GraphEntry = {
    timestamp: string
    total_views: number
    total_cart_adds: number
    total_purchases: number
}

type CategoryEntry = {
    name: string
    revenue: number
    has_increased: boolean
}

type HotProduct = {
    id: string
    name: string
    revenue: number
    category: string
    image?: string
}

export const useDashboardData = () => {
    const [summary, setSummary] = useState<SummaryEntry[]>([])
    const [graph, setGraph] = useState<GraphEntry[]>([])
    const [category, setCategory] = useState<CategoryEntry[]>([])
    const [hotProducts, setHotProducts] = useState<HotProduct[]>([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        const fetchData = async () => {
            try {
                const res = await axios.get('api/v1/dashboard')
                const responseData = res.data.data

                setSummary(responseData.summary)
                setGraph(responseData.graph)
                setCategory(responseData.category)
                setHotProducts(responseData.hot_products)
            } catch (err: unknown) {
                if (isAxiosError(err)) {
                    setError(err.response?.data || 'An error occurred')
                } else {
                    setError('An unexpected error occurred')
                }
            } finally {
                setLoading(false)
            }
        }

        fetchData()
    }, [])

    return { summary, graph, category, hotProducts, loading, error }
}
