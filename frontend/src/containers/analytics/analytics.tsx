import { useEffect, useState } from 'react'
import './analytics.styles.css'
import Loading from '../../components/loading/loading'
import SalesGraph from '../../components/salesgraph/salesgraph'
import { TimeOfDay, useCatalogProductData } from '../../api/hooks/product'

import axiosInstance from '../../api/axios'
import { useParams } from 'react-router'
import ProductDetailsCard from '../../components/productdetailscard/productdetailscard'
import PredictionPanel from '../../components/predictionpanel/predictionpanel'

const Analytics: React.FC = () => {
    const { productId: initialProductId } = useParams<{ productId?: string }>()
    const [productId, setProductId] = useState<string>(
        initialProductId || 'P001',
    )
    const {
        graph,
        averagePurchases,
        product,
        dropdownOptions,
        loading,
        error,
    } = useCatalogProductData(productId)

    const [minDelayDone, setMinDelayDone] = useState(false)
    const [predictionTime, setPredictionTime] = useState<TimeOfDay>()
    const [price, setPrice] = useState<number>(1000)
    const [purchasePrediction, setPurchasePrediction] = useState<number | null>(
        null,
    )
    const [percentage, setPercentage] = useState<number | null>(null)
    const [predictionLoading, setPredictionLoading] = useState(false)
    const [predictionDisabled, setPredictionDisabled] = useState(true)

    useEffect(() => {
        const timer = setTimeout(() => setMinDelayDone(true), 1500)
        return () => clearTimeout(timer)
    }, [])

    useEffect(() => {
        if (product) setPrice(product.base_price)
    }, [product])
    useEffect(
        () => setPredictionDisabled(!(predictionTime && price)),
        [predictionTime, price],
    )

    useEffect(() => {
        if (
            typeof purchasePrediction === 'number' &&
            averagePurchases &&
            predictionTime &&
            typeof averagePurchases[predictionTime] === 'number' &&
            averagePurchases[predictionTime] !== 0
        ) {
            const avg = averagePurchases[predictionTime]
            setPercentage(((purchasePrediction - avg) / avg) * 100)
        } else setPercentage(null)
    }, [purchasePrediction, averagePurchases, predictionTime])

    const handlePredict = () => {
        if (!productId || !predictionTime) return
        setPurchasePrediction(null)
        setPredictionLoading(true)
        setPredictionDisabled(true)
        axiosInstance
            .post('/api/v1/prediction', {
                product_id: productId,
                time_of_day_bucket: predictionTime,
                price,
            })
            .then((res) => setPurchasePrediction(res.data.data.purchases))
            .catch(console.error)
            .finally(() => {
                setPredictionLoading(false)
                setPredictionDisabled(false)
            })
    }

    const handleProductChange = (value: string) => {
        setProductId(value)
        setPurchasePrediction(null)
    }

    if (loading || !product || !minDelayDone) return <Loading />
    if (error) return <p>Error: {error}</p>

    return (
        <div className="analytics">
            <div className="analytics__content">
                <h1>Sale Units Predictor</h1>
                <PredictionPanel
                    productId={productId}
                    dropdownOptions={dropdownOptions}
                    predictionTime={predictionTime}
                    setPredictionTime={setPredictionTime}
                    predictionLoading={predictionLoading}
                    basePrice={product.base_price}
                    price={price}
                    setPrice={setPrice}
                    handlePredict={handlePredict}
                    predictionDisabled={predictionDisabled}
                    purchasePrediction={purchasePrediction}
                    percentage={percentage}
                    handleProductChange={handleProductChange}
                />
            </div>

            <div className="analytics__content">
                <h1>Product Analysis (24 Hr)</h1>
                <div className="analytics__product">
                    <div className="analytics__graph">
                        <SalesGraph salesData={graph} enableToggles={false} />
                    </div>
                    <ProductDetailsCard
                        product={product}
                        productId={productId}
                    />
                </div>
            </div>
        </div>
    )
}

export default Analytics
