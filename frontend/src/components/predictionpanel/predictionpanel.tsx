import { TimeOfDay } from '../../api/hooks/product'
import Dropdown from '../dropdown/dropdown'
import LoadingSpinner from '../loadingspinner/loadingspinner'
import PriceSlider from '../priceslider/priceslider'
import SummaryCard, { convertValueToString } from '../summarycard/summarycard'

import './predictionpanel.styles.css'

const PredictionPanel = ({
    productId,
    dropdownOptions,
    predictionTime,
    setPredictionTime,
    basePrice,
    price,
    setPrice,
    handlePredict,
    predictionDisabled,
    predictionLoading,
    purchasePrediction,
    percentage,
    handleProductChange,
}: any) => (
    <div className="analytics__prediction">
        <div className="analytics__prediction-selectors">
            <div className="analytics__prediction-options">
                <Dropdown
                    values={dropdownOptions}
                    selectedValue={productId}
                    onSelect={handleProductChange}
                />
                <Dropdown
                    values={['Morning', 'Afternoon', 'Evening', 'Overnight']}
                    defaultText="Time of Day Bucket"
                    selectedValue={predictionTime}
                    onSelect={(value) => setPredictionTime(value as TimeOfDay)}
                />
            </div>
            <div className="analytics__prediction-price">
                <PriceSlider
                    basePrice={basePrice}
                    value={price}
                    onChange={setPrice}
                />
                <div className="analytics__prediction-price-value">
                    <h2 className="muted-text">
                        {convertValueToString('revenue', price)}
                    </h2>
                </div>
            </div>
        </div>
        <div className="analytics__prediction-summary">
            <button
                className={`analytics__prediction-button ${predictionDisabled ? 'analytics__prediction-button--disabled' : ''}`}
                onClick={handlePredict}
                disabled={predictionDisabled}
            >
                <h2>PREDICT</h2>
            </button>
            {predictionLoading ? (
                <div className="analytics__prediction-loading">
                    <LoadingSpinner />
                </div>
            ) : predictionDisabled && purchasePrediction === null ? (
                <div className="analytics__prediction-placeholder">
                    <p>Fill in the fields!</p>
                </div>
            ) : purchasePrediction === null ? (
                <div className="analytics__prediction-placeholder">
                    <p>Click on PREDICT!</p>
                </div>
            ) : (
                <SummaryCard
                    title="Purchases"
                    focusPercentage={percentage}
                    focusValue={purchasePrediction || 0}
                />
            )}
        </div>
    </div>
)

export default PredictionPanel
