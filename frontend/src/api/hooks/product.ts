import { useState, useEffect } from 'react'
import { isAxiosError } from 'axios'
import axios from '../axios'

type ProductDetails = {
    product_id: string
    product_name: string
    product_image: string
    average_rating: number
    revenue: number
    category: string
    base_price: number
    total_purchases: number
    total_views: number
    total_cart_adds: number
}

type GraphEntry = {
    timestamp: string
    views: number
    cart_adds: number
    purchases: number
}

type GraphData = {
    timestamp: string
    total_views: number
    total_cart_adds: number
    total_purchases: number
}

export type TimeOfDay = 'Morning' | 'Afternoon' | 'Evening' | 'Overnight'

type AveragePurchases = Record<TimeOfDay, number>

export const useCatalogProductData = (productId: string) => {
    const [product, setProduct] = useState<ProductDetails | null>(null)
    const [averagePurchases, setAveragePurchases] =
        useState<AveragePurchases | null>(null)
    const [dropdownOptions, setDropdownOptions] = useState<string[]>([])
    const [graph, setGraph] = useState<GraphData[]>([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        const fetchProduct = async () => {
            try {
                const res = await axios.get(`/api/v1/catalog/${productId}`)
                const rawData = res.data.data

                const transformedGraph: GraphData[] = rawData.graph.map(
                    (entry: GraphEntry) => ({
                        timestamp: entry.timestamp,
                        total_views: entry.views,
                        total_cart_adds: entry.cart_adds,
                        total_purchases: entry.purchases,
                    }),
                )

                setProduct(rawData.details)
                setAveragePurchases(rawData.average_purchases)
                setGraph(transformedGraph)

                const catalogRes = await axios.get('/api/v1/catalog/')

                const catalogData = catalogRes.data.data
                const allProducts: string[] = Object.values(catalogData)
                    .flat()
                    .map((p) => (p as ProductDetails).product_id)
                    .sort((a, b) => {
                        const numA = parseInt(a.replace(/\D/g, ''), 10)
                        const numB = parseInt(b.replace(/\D/g, ''), 10)
                        return numA - numB
                    })

                setDropdownOptions(allProducts)
            } catch (err: unknown) {
                if (isAxiosError(err)) {
                    setError(
                        err.response?.data ||
                            'An error occurred while fetching product data.',
                    )
                } else {
                    setError('An unexpected error occurred')
                }
            } finally {
                setLoading(false)
            }
        }

        fetchProduct()
    }, [productId])

    return { graph, averagePurchases, product, dropdownOptions, loading, error }
}
