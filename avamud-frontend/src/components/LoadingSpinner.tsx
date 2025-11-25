// src/components/LoadingSpinner.tsx

import styles from './LoadingSpinner.module.css';

export const LoadingSpinner: React.FC = () => {
  return (
    <div className={styles.spinner}>
      <div className={styles.dot}></div>
      <p>Carregando...</p>
    </div>
  );
};
