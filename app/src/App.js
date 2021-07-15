import "./App.css";
import "bootstrap/dist/css/bootstrap.min.css";
import { Button } from "react-bootstrap";
import { makeStyles } from "@material-ui/core/styles";
import { TextField } from "@material-ui/core";
import { useCallback, useMemo, useState } from "react";

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
  const handleRun = useCallback((algo) => {
    const stringInput = generateString;
    console.log(algo)
    console.log(stringInput)
  },[generateString])
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
					onChange={event => setNumberOfBranches(event.target.value * 1)}
				/>
				<TextField
					id="filled-basic"
					label="No. Requests"
					variant="filled"
					size="small"
					type="number"
					onChange={event => setNumberOfRquests(event.target.value * 1)}
				/>
				<TextField
					id="outlined-basic"
					label="No. Services"
					variant="filled"
					size="small"
					type="number"
					onChange={event => setNumberOfServices(event.target.value * 1)}
				/>
				<TextField
					id="outlined-basic"
					label="Maximum Distance"
					variant="filled"
					size="small"
					type="number"
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
			{numberOfBranches > 0 && [...Array(numberOfBranches)].map((e, i) => {
				return (
					<>
						<form
							className={classes.root1}
							noValidate
							autoComplete="off"
							key={`branch-${i}`}
						>
							{numberOfServices > 0 && [...Array(numberOfServices)].map((e, j) => {
								return (
									<TextField
										id={`branch-${i}-service-${j}`}
										key={`branch-${i}-service-${j}`}
										label={`Service ${j + 1} at Branch ${i + 1}`}
										variant="filled"
										size="small"
										type="number"
										onChange={event =>
											setTimeForService(i, j, event.target.value * 1)
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
												id={`branch-${i}-info-${j}`}
												key={`branch-${i}-info-${j}`}
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
															id={`branch-${i}-info-${j}`}
															key={`branch-${i}-info-${j}`}
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
			<Button onClick={() => handleRun("meta-heuristic")} variant="success">Meta Heuristic</Button>{" "}
			<Button onClick={() => handleRun("dp")} variant="danger">DP</Button>
		</div>
	);
}

export default App;