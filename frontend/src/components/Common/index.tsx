import React from 'react';

export const Badge: React.FC<{ children: React.ReactNode, variant?: 'success' | 'warning' | 'danger' | 'info' | 'primary' }> = ({ children, variant = 'primary' }) => (
  <span className={`badge badge-${variant}`}>{children}</span>
);

export const Loader: React.FC<{ message?: string }> = ({ message = 'Analyzing...' }) => (
  <div className="loader-container">
    <div className="spinner"></div>
    <p>{message}</p>
  </div>
);

export const Tooltip: React.FC<{ text: string, children: React.ReactNode }> = ({ text, children }) => (
  <div className="tooltip-container">
    {children}
    <div className="tooltip-content">{text}</div>
  </div>
);
