import profiteer from '../../assets/logos/profiteer.svg'
import './loading.styles.css'

const Loading: React.FC = () => {
    return (
        <div className="loading">
            <img
                src={profiteer}
                alt="Profiteer Logo"
                className="loading__logo"
            />
        </div>
    )
}

export default Loading
