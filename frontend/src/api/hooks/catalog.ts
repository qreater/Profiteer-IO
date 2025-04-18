import { useState, useEffect } from 'react'
import { isAxiosError } from 'axios'
import axios from '../axios'

export type CatalogProduct = {
    product_id: string
    product_name: string
    product_image: string
    average_rating: number
    revenue: number
}

type CatalogData = {
    [category: string]: CatalogProduct[]
}

export const useCatalogData = () => {
    const [catalog, setCatalog] = useState<CatalogData>({})
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        const fetchCatalog = async () => {
            try {
                const res = await axios.get('/api/v1/catalog/')
                const responseData = res.data.data

                setCatalog(responseData)
            } catch (err: unknown) {
                if (isAxiosError(err)) {
                    setError(
                        err.response?.data ||
                            'An error occurred while fetching catalog data.',
                    )
                } else {
                    setError('An unexpected error occurred')
                }
            } finally {
                setLoading(false)
            }
        }

        fetchCatalog()
    }, [])

    return { catalog, loading, error }
}
