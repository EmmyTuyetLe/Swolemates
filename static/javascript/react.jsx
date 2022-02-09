function UpdateButton(props) {
    return (
      <div>
        <button type="button" style={{backgroundColor: '#FCBAD3', color: 'white'}}>
          {props.message}
        </button>
      </div>
    );
  }
  
  ReactDOM.render(<UpdateButton message='Update your profile' />, document.querySelector('#button'));
