function UpdateButton(props) {
    return (
      <div>
        <button type="button" style={{backgroundColor: '#92D293', color: 'white'}}>
          {props.message}
        </button>
      </div>
    );
  }
  
  ReactDOM.render(<UpdateButton message='Update' />, document.querySelector('#button'));
