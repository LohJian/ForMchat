import React from 'react';
import styles from '../styles/ProfilePage.module.css';

export default function InterestTags({ tags }) {
  return (
    <div className={styles.tagsContainer}>
      {tags.map((tag, index) => (
        <span key={index} className={styles.tag}>
          #{tag}
        </span>
      ))}
    </div>
  );
}