import { useEffect, useState } from 'react'
import Loading from '../../components/loading/loading'

import { useCatalogData } from '../../api/hooks/catalog'
import ProductCarousel from '../../components/productcarousel/productcarousel'
import { TagIcon } from '@heroicons/react/24/solid'

import './catalog.styles.css'

const Catalog: React.FC = () => {
    const [minDelayDone, setMinDelayDone] = useState(false)
    const { catalog, loading, error } = useCatalogData()

    useEffect(() => {
        const timer = setTimeout(() => {
            setMinDelayDone(true)
        }, 1500)
        return () => clearTimeout(timer)
    }, [])

    if (loading || !minDelayDone) {
        return <Loading />
    }

    if (error) return <p>Error: {error}</p>

    return (
        <div className="catalog">
            {Object.entries(catalog).map(([category, products]) => (
                <div key={category} className="catalog__section">
                    <div className="catalog__header">
                        <TagIcon className="catalog__icon text-accent" />
                        <h1>{category}</h1>
                    </div>
                    <ProductCarousel products={products} />
                </div>
            ))}
        </div>
    )
}

export default Catalog
