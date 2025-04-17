import React from 'react'

import { Route, Routes } from 'react-router'
import { BrowserRouter } from 'react-router-dom'

import Layout from './components/layout/layout'
import Dashboard from './containers/dashboard/dashboard'

const App: React.FC = () => {
    return (
        <>
            <BrowserRouter>
                <Layout>
                    <Routes>
                        <Route path="/" element={<Dashboard />} />
                    </Routes>
                </Layout>
            </BrowserRouter>
        </>
    )
}

export default App
