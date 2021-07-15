import "./App.css";
import "bootstrap/dist/css/bootstrap.min.css";
import { Button } from "react-bootstrap";
import { makeStyles } from "@material-ui/core/styles";
import { TextField } from "@material-ui/core";
import { useCallback, useMemo, useRef, useState } from "react";
import axios from 'axios';
import ResultTable from "./ResultTable";
import * as XLSX from 'xlsx';

const useStyles = makeStyles(theme => ({
	root: {
		"& > *": {
			margin: theme.spacing(1),
			width: "20ch"
		}
	},
	root1: {
		"& > *": {
			margin: theme.spacing(1),
			width: "20ch"
			// fontSize:'10px'
		}
	}
}));

function App() {
	const classes = useStyles();
	const [numberOfBranches, setNumberOfBranches] = useState(0);
	const [numberOfRequests, setNumberOfRquests] = useState(0);
	const [numberOfServices, setNumberOfServices] = useState(0);
	const [maxDistance, setMaxDistance] = useState(0);
	const [timeNeeded, setTimeNeeded] = useState({});
	const [requestsInfo, setRequestsInfo] = useState({});
	const [branchesInfo, setBranchesInfo] = useState({});
	const [countersCount, setCountersCount] = useState({});
	const [countersInfo, setCountersInfo] = useState({});
	const [results, setResults] = useState([]);
  const [fileInput, setFIleInput] = useState('');
  const ref = useRef();

  // process CSV data
  const processData = dataString => {
    const dataStringLines = dataString.split(/\r\n|\n/);

    let stringInput = "";
    for (let i = 0; i < dataStringLines.length; i++) {
      const row = dataStringLines[i].split(/,(?![^"]*"(?:(?:[^"]*"){2})*[^"]*$)/);
      for( let string of row) {
        stringInput+= string + " "
      }
      stringInput += "\n"
    }
    setFIleInput(stringInput)
  }

  // handle file upload
  const handleFileUpload = e => {
    const file = e.target.files[0];
    const reader = new FileReader();
    reader.onload = (evt) => {
      /* Parse data */
      const bstr = evt.target.result;
      const wb = XLSX.read(bstr, { type: 'binary' });
      /* Get first worksheet */
      const wsname = wb.SheetNames[0];
      const ws = wb.Sheets[wsname];
      /* Convert array of arrays */
      const data = XLSX.utils.sheet_to_csv(ws, { header: 1 });
      processData(data);
    };
    reader.readAsBinaryString(file);
  }

	const setTimeForService = useCallback(
		(branch, service, time) => {
			let newTimeNeeded = JSON.parse(JSON.stringify(timeNeeded));
			newTimeNeeded[`${branch}${service}`] = time;
			setTimeNeeded(newTimeNeeded);
		},
		[timeNeeded]
	);
	const setRequestInfo = useCallback(
		(requestNumber, variable, input) => {
			let newRequestsInfo = JSON.parse(JSON.stringify(requestsInfo));
			newRequestsInfo[`${requestNumber}${variable}`] = input;
			setRequestsInfo(newRequestsInfo);
		},
		[requestsInfo]
	);
	const setBranchInfo = useCallback(
		(branchNumber, variable, input) => {
			let newRequestsInfo = JSON.parse(JSON.stringify(branchesInfo));
			newRequestsInfo[`${branchNumber}${variable}`] = input;
			setBranchesInfo(newRequestsInfo);
		},
		[branchesInfo]
	);
	const setCounterCount = useCallback(
		(branchNumber, counterNumber, input) => {
			let newRequestsInfo = JSON.parse(JSON.stringify(countersCount));
			newRequestsInfo[`${branchNumber}${counterNumber}`] = input;
			setCountersCount(newRequestsInfo);
		},
		[countersCount]
	);
	const setCounterInfo = useCallback(
		(branchNumber, counterNumber, serviceIndx, input) => {
			let newRequestsInfo = JSON.parse(JSON.stringify(countersInfo));
			newRequestsInfo[`${branchNumber}${counterNumber}${serviceIndx}`] = input;
			setCountersInfo(newRequestsInfo);
		},
		[countersInfo]
	);
	const reset = useCallback(() => {
    setNumberOfBranches(0)
    setNumberOfRquests(0)
    setNumberOfServices(0)
    setMaxDistance(0)
    setTimeNeeded({})
    setRequestsInfo({})
    setBranchesInfo({})
    setCountersCount({})
    setCountersInfo({})
    setResults([])
		},
		[]
	);
  const generateString = useMemo(() => {
    let stringInput = numberOfBranches + " " + numberOfRequests + " " + numberOfServices + " " + maxDistance +"\n";
    let  i = 0, j = 0;
    while(i < numberOfServices) {
      j = 0;
      while(j < numberOfBranches) {
        stringInput += timeNeeded[`${j}${i}`] + " "
        j++;
      }
      stringInput += "\n"
      i++;
    }
    i = 0;
    while( i < numberOfRequests) {
      stringInput += requestsInfo[`${i}0`] + " " + requestsInfo[`${i}1`] + " " + requestsInfo[`${i}2`] + " " + requestsInfo[`${i}3`] + "\n"
      i++;
    }
    i = 0;
    while(i < numberOfBranches) {
      stringInput += branchesInfo[`${i}0`] + " " + branchesInfo[`${i}1`] + " " + branchesInfo[`${i}2`] + " " + branchesInfo[`${i}3`] + "\n"
      let counterCount = branchesInfo[`${i}3`];
      j = 0;
      while(j < counterCount) {
        stringInput += countersCount[`${i}${j}`]
        let  k = 0;
        while( k < countersCount[`${i}${j}`]) {
          stringInput += " " + countersInfo[`${i}${j}${k}`]
          k++;
        }
        stringInput += "\n"
        j++;
      }
      i++;
    }
    return stringInput
  },[numberOfBranches, numberOfRequests, numberOfServices, timeNeeded, requestsInfo, branchesInfo, countersCount, countersInfo, maxDistance])
  const handleRun = useCallback( async (algo) => {
    const stringInput = fileInput === '' ? generateString : fileInput;
    const res = await axios.post(`http://localhost:5000/${algo}`, {data: stringInput})
    const outputRecieved = res.data
    let outputs = outputRecieved.split("#");
    let results = []
    for(let output of outputs) {
      let array = output.split("\n");
      results.append({matches: array[0], requests: array.slice(1)})
    }
    setResults(results)
    ref.current.value = ""
  },[generateString, fileInput])
	return (
		<div className="App">
			<h1>Balck Opt - Bank Reservation System</h1>
			<form className={classes.root} noValidate autoComplete="off">
				<TextField
					id="standard-basic"
					label="No. Branches"
					variant="filled"
					size="small"
					type="number"
          value={numberOfBranches}
					onChange={event => setNumberOfBranches(event.target.value * 1)}
				/>
				<TextField
					id="filled-basic"
					label="No. Requests"
					variant="filled"
					size="small"
					type="number"
          value={numberOfRequests}
					onChange={event => setNumberOfRquests(event.target.value * 1)}
				/>
				<TextField
					id="outlined-basic"
					label="No. Services"
					variant="filled"
					size="small"
					type="number"
          value={numberOfServices}
					onChange={event => setNumberOfServices(event.target.value * 1)}
				/>
				<TextField
					id="outlined-basic"
					label="Maximum Distance"
					variant="filled"
					size="small"
					type="number"
          value={maxDistance}
					onChange={event => setMaxDistance(event.target.value * 1)}
				/>
			</form>
			{numberOfBranches > 0 && numberOfServices > 0 && (
				<>
					<hr />
					<h3 style={{ fontWeight: "normal", fontSize: "18px" }}>
						Time Needed For
					</h3>
				</>
			)}
			{numberOfServices > 0 && [...Array(numberOfServices)].map((e, i) => {
				return (
					<>
						<form
							className={classes.root1}
							noValidate
							autoComplete="off"
							key={`branch-${i}`}
						>
							{numberOfBranches > 0 && [...Array(numberOfBranches)].map((e, j) => {
								return (
									<TextField
										id={`branch-${i}-service-${j}`}
										key={`branch-${i}-service-${j}`}
										label={`Service ${i + 1} at Branch ${j + 1}`}
										variant="filled"
										size="small"
										type="number"
										onChange={event =>
											setTimeForService(j, i, event.target.value * 1)
										}
									/>
								);
							})}
						</form>
					</>
				);
			})}
			{numberOfRequests > 0 && (
				<>
					<hr />
					<h3 style={{ fontWeight: "normal", fontSize: "18px" }}>
						Requests Data
					</h3>
				</>
			)}
			{numberOfRequests > 0 && [...Array(numberOfRequests)].map((e, i) => {
				return (
					<>
						<form
							className={classes.root1}
							noValidate
							autoComplete="off"
							key={`request-${i}`}
						>
							{[...Array(4)].map((e, j) => {
								return (
									<TextField
										id={`request-${i}-${j}`}
										key={`request-${i}-${j}`}
										label={
											`Request ${i + 1} ` +
											(j === 0
												? "X-Location"
												: j === 1
												? "Y-Location"
												: j === 2
												? "Priority"
												: "Service")
										}
										variant="filled"
										size="small"
										type="number"
										onChange={event =>
											setRequestInfo(i, j, event.target.value * 1)
										}
									/>
								);
							})}
						</form>
					</>
				);
			})}
			{numberOfBranches > 0 && (
				<>
					<hr />
					<h3 style={{ fontWeight: "normal", fontSize: "18px" }}>
						Branches Information
					</h3>
				</>
			)}
			{numberOfBranches > 0 && [...Array(numberOfBranches)].map((e, i) => {
				return (
					<>
						<form
							className={classes.root1}
							noValidate
							autoComplete="off"
							key={`branch-${i}`}
						>
							{[...Array(4)].map((e, j) => {
								return (
									<TextField
										id={`branch-${i}-info-${j}`}
										key={`branch-${i}-info-${j}`}
										label={
											`Branch ${i + 1} ` +
											(j === 0
												? "X-Location"
												: j === 1
												? "Y-Location"
												: j === 2
												? "Slots"
												: "Counters")
										}
										variant="filled"
										size="small"
										type="number"
										onChange={event =>
											setBranchInfo(i, j, event.target.value * 1)
										}
									/>
								);
							})}
							<br />
							{branchesInfo[`${i}3`] > 0 &&
								[...Array(branchesInfo[`${i}3`])].map((e, j) => {
									return (
										<>
											<TextField
												id={`branch-${i}-counters-${j}`}
												key={`branch-${i}-counters-${j}`}
												label={`Counter ${i + 1} Services No.`}
												variant="filled"
												size="small"
												type="number"
												onChange={event =>
													setCounterCount(i, j, event.target.value * 1)
												}
											/>
											{countersCount[`${i}${j}`] > 0 &&
												[...Array(countersCount[`${i}${j}`])].map((e, k) => {
													return (
														<TextField
															id={`counter-${i}-info-${j}`}
															key={`counter-${i}-info-${j}`}
															label={`Services ${k + 1}`}
															variant="filled"
															size="small"
															type="number"
															onChange={event =>
																setCounterInfo(i, j, k, event.target.value * 1)
															}
														/>
													);
												})}
											<br />
										</>
									);
								})}
						</form>
						<hr />
					</>
				);
			})}
			<Button onClick={() => handleRun("baseline")} variant="primary">Baseline</Button>{" "}
			<Button onClick={() => handleRun("mip")} variant="secondary">MIP</Button>{" "}
			<Button onClick={() => handleRun("meta")} variant="success">Meta Heuristic</Button>{" "}
			<Button onClick={() => handleRun("dp")} variant="danger">DP</Button>{" "}
			<Button onClick={reset} variant="warning">Reset</Button> {" "}
      <input ref={ref} type="file" accept=".csv" onChange={handleFileUpload}/>
      <hr/>
      <h3 style={{ fontWeight: "800", fontSize: "22px" }}>
        Outputs
      </h3>
      {results.map(({matches, output}, i)=>
        <div key={i}>
          <h3 style={{ fontWeight: "600", fontSize: "18px" }}>
            Number of Matches: {matches}
          </h3>
          <ResultTable output={output}/>
        </div>
      )}
		</div>
	);
}

export default App;
