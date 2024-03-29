import React from 'react';
import Header from './Header';
import Menu from './Menu';

const Layout = ({ children }) => {
  return (
    <div>
      <Header />
      <Menu />
      <main>{children}</main>
    </div>
  );
};

export default Layout;
