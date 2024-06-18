import React, { useEffect, useState } from 'react'

import api from '../../api'
import styles from './style.module.css'
import { NavFPK, Container } from '../index.js'

const Header = () => {
  const [userName, setUserName] = useState('Не определен')
  const [macLabel, setMacLabel] = useState('')

  useEffect((_) => {
    api
    .getMacLabel()
    .then((res) => {
      {res['REMOTE_USER'] !== null ? setUserName(res['REMOTE_USER']): ''}
      setMacLabel(res['Mac-Label']);
    })
    }, [])

  return (
    <header className={styles.header}>
      <Container>
        <div className={styles.headerContent}>
          <NavFPK />
        </div>
      </Container>
      <div style={{color: 'white', paddingRight: '45px', fontSize:'15px', whiteSpace: 'nowrap'}}>{userName} | {macLabel}</div>
    </header>
  )
}

export default Header
