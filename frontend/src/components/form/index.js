import cn from 'classnames'

import styles from './style.module.css'

const Form = ({ children, className, onSubmit }) => {
  return (
    <form className={cn(styles.form, className)} onSubmit={onSubmit}>
      {children}
    </form>
  );
};

export default Form;
