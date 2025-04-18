import React from 'react'

import { Route, Routes } from 'react-router'
import { BrowserRouter } from 'react-router-dom'

import Layout from './components/layout/layout'
import Dashboard from './containers/dashboard/dashboard'
import Catalog from './containers/catalog/catalog'

const App: React.FC = () => {
    return (
        <>
            <BrowserRouter>
                <Layout>
                    <Routes>
                        <Route path="/" element={<Dashboard />} />
                        <Route path="/catalog" element={<Catalog />} />
                    </Routes>
                </Layout>
            </BrowserRouter>
        </>
    )
}

export default App
