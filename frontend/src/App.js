import React, { useState } from 'react';
import { Layout, Menu, theme, ConfigProvider, Card, Statistic, Row, Col } from 'antd';
import { 
  DashboardOutlined, 
  AnalysisOutlined, 
  BarChartOutlined, 
  BulbOutlined, 
  FileTextOutlined 
} from '@ant-design/icons';
import { BrowserRouter, Routes, Route, Navigate, useNavigate, useLocation } from 'react-router-dom';
import zhCN from 'antd/locale/zh_CN';
import Dashboard from './pages/Dashboard';
import Analysis from './pages/Analysis';
import Comparison from './pages/Comparison';
import Suggestions from './pages/Suggestions';
import Reports from './pages/Reports';

const { Header, Content, Footer, Sider } = Layout;

const AppContent = () => {
  const [collapsed, setCollapsed] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();
  
  const menuItems = [
    { key: '/dashboard', icon: <DashboardOutlined />, label: '数据总览' },
    { key: '/analysis', icon: <AnalysisOutlined />, label: '评价分析' },
    { key: '/comparison', icon: <BarChartOutlined />, label: '竞品对比' },
    { key: '/suggestions', icon: <BulbOutlined />, label: '改进建议' },
    { key: '/reports', icon: <FileTextOutlined />, label: '报告下载' },
  ];

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Sider 
        collapsible 
        collapsed={collapsed} 
        onCollapse={setCollapsed}
        theme="dark"
        style={{
          overflow: 'auto',
          height: '100vh',
          position: 'fixed',
          left: 0,
          top: 0,
          bottom: 0,
        }}
      >
        <div style={{ 
          height: 64, 
          display: 'flex', 
          alignItems: 'center', 
          justifyContent: 'center',
          color: 'white',
          fontSize: collapsed ? 16 : 20,
          fontWeight: 'bold',
          borderBottom: '1px solid rgba(255,255,255,0.1)'
        }}>
          {collapsed ? 'PA' : '产品分析'}
        </div>
        <Menu
          theme="dark"
          mode="inline"
          selectedKeys={[location.pathname]}
          items={menuItems}
          onClick={({ key }) => navigate(key)}
        />
      </Sider>
      <Layout style={{ marginLeft: collapsed ? 80 : 200, transition: 'all 0.2s' }}>
        <Header style={{ 
          padding: '0 24px', 
          background: '#fff', 
          display: 'flex', 
          alignItems: 'center',
          boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
          position: 'sticky',
          top: 0,
          zIndex: 1
        }}>
          <h2 style={{ margin: 0, color: '#1890ff' }}>产品评价数据分析系统</h2>
        </Header>
        <Content style={{ margin: 24 }}>
          <div style={{ padding: 24, background: '#f0f2f5', minHeight: 360 }}>
            <Routes>
              <Route path="/" element={<Navigate to="/dashboard" replace />} />
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/analysis" element={<Analysis />} />
              <Route path="/comparison" element={<Comparison />} />
              <Route path="/suggestions" element={<Suggestions />} />
              <Route path="/reports" element={<Reports />} />
            </Routes>
          </div>
        </Content>
        <Footer style={{ textAlign: 'center', background: '#001529', color: 'rgba(255,255,255,0.65)' }}>
          产品评价数据分析系统 ©2026 Created by CodeBuddy
        </Footer>
      </Layout>
    </Layout>
  );
};

const App = () => {
  return (
    <ConfigProvider locale={zhCN}>
      <BrowserRouter>
        <AppContent />
      </BrowserRouter>
    </ConfigProvider>
  );
};

export default App;
