import cn from 'classnames'

import { useEffect, useState } from 'react'

import styles from './style.module.css'

const Input = ({
  onChange,
  placeholder,
  label,
  type = 'text',
  inputClassName,
  labelClassName,
  className,
  name,
  required,
  onFocus,
  onBlur,
  value = ''
}) => {
  const [inputValue, setInputValue] = useState(value);
  const handleValueChange = (e) => {
    const value = e.target.value;
    setInputValue(value);
    onChange(e);
  };
  useEffect(
    (_) => {
      if (value !== inputValue) {
        setInputValue(value);
      }
    },
    [value]
  );

  return (
    <div className={cn(styles.input, className)}>
      <label className={styles.inputLabel}>
        {label && <div className={cn(styles.inputLabelText, labelClassName)}>{label}</div>}
        <input title={placeholder}
          type={type}
          required={required}
          name={name}
          // placeholder={placeholder}
          className={cn(styles.inputField, inputClassName)}
          onChange={(e) => {
            handleValueChange(e);
          }}
          onFocus={onFocus}
          value={inputValue}
          onBlur={onBlur}
        />
      </label>
    </div>
  );
};

export default Input;
