import React from 'react';
import styles from '../styles/ProfilePage.module.css';

export default function PhotoGallery({ photos }) {
  return (
    <div className={styles.photoGallery}>
      {photos.map((photo, index) => (
        <div 
          key={index}
          className={styles.photoItem}
          style={{ backgroundImage: `url(${photo})` }}
        />
      ))}
    </div>
  );
}