const express = require("express");
const cors = require("cors");
const multer = require("multer");
const path = require("path");
const bodyParser = require("body-parser");
const { spawn } = require("child_process");
const { exec } = require('child_process');

const app = express();
const PORT = 5000;

app.use(cors());
app.use(express.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, "public")));

// ...................................................... Basic ROUTES...................................................//
app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "index.html"));
});

app.get("/viewdetails", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "LoginDetails.html"));
});

app.get("/ChatPage", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "ChatPage.html"));  
});

app.get("/SignUP", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "SignUPPage.html"));
});

// ...................................................... Software search Routes...................................................//
app.get("/QuestionAnswering", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "QuestionAnswering-1.html"));
});
// >>>>>>>>>>>> For QuestionAnswering-1 software <<<<<<<<<<<<<<<<<<<<<<
app.post('/ask', (req, res) => {
    const { question, context } = req.body;

    if (!question) {
        return res.status(400).json({ error: 'Question is required' });
    }

    const command = `python QuestionAnswerSoftware.py "${question}" "${context}"`;

    const pythonProcess = spawn(command, { shell: true, stdio: 'pipe' });

    pythonProcess.stdout.on('data', (data) => {
        const answer = data.toString().trim();
        if (!res.headersSent) {
            res.json({ answer });
        }
    });

    pythonProcess.stderr.on('data', (error) => {
        console.error(`Error: ${error.toString()}`);
        if (!res.headersSent) {
            res.status(500).json({ error: 'Internal Server Error' });
        }
    });

    pythonProcess.on('error', (error) => {
        console.error(`Execution Error: ${error}`);
        if (!res.headersSent) {
            res.status(500).json({ error: 'Failed to execute Python script' });
        }
    });
});


// >>>>>>>>>>>>>>>>> For QuestionAnswering-1 software <<<<<<<<<<<<<<<<<<<<<<

//......................................................................StudyNotesGenerator .....................................//
app.get("/StudyNotesGenerator", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "StudyNotesGenerator-2.html"));
});
// >>>>>>>>>>>>>>>>> StudyNotesGenerator software <<<<<<<<<<<<<<<<<<<<<<

app.post('/studynotes', (req, res) => {
  const topic = req.body.topic;

  if (!topic) {
    return res.status(400).json({ error: 'No topic provided' });
  }

  const python = spawn('py', ['studynotes.py', topic]); // ⬅️ key fix here

  let dataToSend = '';
  python.stdout.on('data', (data) => {
    dataToSend += data.toString();
  });

  python.stderr.on('data', (data) => {
    console.error(`stderr: ${data}`);
  });

  python.on('close', (code) => {
    if (code !== 0) {
      return res.status(500).json({ error: 'Python script error' });
    }

    res.json({ answer: dataToSend.trim() });
  });
});


// >>>>>>>>>>>>>>>>> StudyNotesGenerator software <<<<<<<<<<<<<<<<<<<<<<
//......................................................................StudyNotesGenerator .....................................//

//...................................................................... TextSummarization .....................................//
app.get("/TextSummarization", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "TextSummarization-3.html"));
});
// >>>>>>>>>>>>>>>>> TextSummarization software <<<<<<<<<<<<<<<<<<<<<<
app.post("/summarize", (req, res) => {
  const { text, summary_length, include_key_points, use_bullet_points } = req.body
  //console.log(text)
  //console.log(summary_length)
  //console.log(include_key_points)
  //console.log(use_bullet_points)
  //$$$$$$$$$$$$$$$$$$$$$ Data push on py file $$$$$$$$$$$$$$$$$$$$$$
  const { spawn } = require('child_process');

  const pythonProcess = spawn('python', [
    'TextSummarizationSoftware.py',
    text,
    summary_length,
    include_key_points,
    use_bullet_points
]);
  //$$$$$$$$$$$$$$$$$$$$$ Data push on py file $$$$$$$$$$$$$$$$$$$$$$

//$$$$$$$$$$$$$$$$$$$$$$$$$ Get result from .py & push data on html $$$$$$$$$$$$$$$$$$$$
let result = "";
pythonProcess.stdout.on('data', (data) => {
  result += data.toString();
});
pythonProcess.stderr.on('data', (data) => {
  console.error(`Python error: ${data}`);
});
pythonProcess.on('close', (code) => {
  if (code !== 0) {
    return res.status(500).json({ error: "Python script failed." });
  }
  res.json({ answer: result.trim() });  // Return to frontend
});
//$$$$$$$$$$$$$$$$$$$$$$$$$ Get result from .py & push data on html $$$$$$$$$$$$$$$$$$$$
});
// >>>>>>>>>>>>>>>>> TextSummarization software <<<<<<<<<<<<<<<<<<<<<<
//...................................................................... TextSummarization .....................................//

//...................................................................... StudyPlanGenerator .....................................//
app.get("/StudyPlanGenerator", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "StudyPlanGenerator-4.html"));
});
// >>>>>>>>>>>>>>>>> StudyPlanGenerator software <<<<<<<<<<<<<<<<<<<<<<
app.post("/StudyPlanGenerator", (req, res) => {
  const { SubjectName, Topic, Date, DailyStudyHRS } = req.body
  //console.log(SubjectName)
  //console.log(Topic)
  //console.log(Date)
  //console.log(DailyStudyHRS)
   //$$$$$$$$$$$$$$$$$$$$$ Data push on py file $$$$$$$$$$$$$$$$$$$$$$
  const { spawn } = require('child_process');

  const pythonProcess = spawn('python', [
    'StudyPlanGenerator.py',
    SubjectName,
    Topic,
    Date,
    DailyStudyHRS
]);
  //$$$$$$$$$$$$$$$$$$$$$ Data push on py file $$$$$$$$$$$$$$$$$$$$$$
  //$$$$$$$$$$$$$$$$$$$$$$$$$ Get result from .py & push data on html $$$$$$$$$$$$$$$$$$$$
let result = "";
pythonProcess.stdout.on('data', (data) => {
  result += data.toString();
});
pythonProcess.stderr.on('data', (data) => {
  console.error(`Python error: ${data}`);
});
pythonProcess.on('close', (code) => {
  if (code !== 0) {
    return res.status(500).json({ error: "Python script failed." });
  }
  res.json({ answer: result.trim() });  // Return to frontend
});
//$$$$$$$$$$$$$$$$$$$$$$$$$ Get result from .py & push data on html $$$$$$$$$$$$$$$$$$$$
});
// >>>>>>>>>>>>>>>>> StudyPlanGenerator software <<<<<<<<<<<<<<<<<<<<<<
//...................................................................... StudyPlanGenerator .....................................//

//...................................................................... MockExamQuestions .....................................//
app.get("/MockExamQuestions", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "MockExamQuestions-5.html"));
});
// >>>>>>>>>>>>>>>>> MockExamQuestionsSoftware <<<<<<<<<<<<<<<<<<<<<<
app.post("/MockExamQuestions", (req, res) => {
  const { subject, topics, difficulty, questionType, numQuestions } = req.body;

  //console.log("Received data from client:");
  //console.log("Subject:", subject);
  //console.log("Topics:", topics);
  //console.log("Difficulty:", difficulty);
  //console.log("Question Type:", questionType);
  //console.log("Number of Questions:", numQuestions);

  const pythonProcess = spawn('python', [
    'MockExamQuestionsSoftware.py',
    subject,
    topics.join(','),      
    difficulty,
    questionType,
    numQuestions.toString()
  ]);

  let result = "";
  pythonProcess.stdout.on('data', (data) => {
    result += data.toString();
  });

  pythonProcess.stderr.on('data', (data) => {
    console.error(`Python error: ${data}`);
  });

  pythonProcess.on('close', (code) => {
    if (code !== 0) {
      return res.status(500).json({ error: "Python script failed." });
    }
    //console.log("Python output:", result);
    res.json({ output: result.trim() }); 
  });
});
// >>>>>>>>>>>>>>>>> MockExamQuestionsSoftware <<<<<<<<<<<<<<<<<<<<<<
//...................................................................... MockExamQuestions .....................................//

//...................................................................... PDF-Analysis .....................................//
app.get("/PDF-Analysis", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "PDF-Analysis-6.html"));
});
// >>>>>>>>>>>>>>>>> PDF-Analysis Software <<<<<<<<<<<<<<<<<<<<<<
const upload = multer({ dest: "uploads/" });
app.post("/analyze", upload.single("pdf"), (req, res) => {
    const pdfPath = req.file.path;
    const analysisType = req.body.analysisType || "Summary";
    const includeExamples = req.body.includeExamples === "true" ? "yes" : "no";
    const includeDefinitions = req.body.includeDefinitions === "true" ? "yes" : "no";
    const formatType = req.body.format || "markdown";

    const pythonProcess = spawn("python3", [
        "AnalyzePDFSoftware.py",
        pdfPath,
        analysisType,
        includeExamples,
        includeDefinitions,
        formatType
    ]);

    let output = "";
    let errorOutput = "";

    pythonProcess.stdout.on("data", (data) => {
        output += data.toString();
    });

    pythonProcess.stderr.on("data", (data) => {
        errorOutput += data.toString();
    });

    pythonProcess.on("close", (code) => {
        fs.unlink(pdfPath, () => {}); // Delete uploaded PDF after processing

        if (code === 0) {
            res.status(200).send({ result: output });
        } else {
            res.status(500).send({ error: errorOutput || "Python script error" });
        }
    });
});
// >>>>>>>>>>>>>>>>> PDF-Analysis Software <<<<<<<<<<<<<<<<<<<<<<
//...................................................................... PDF-Analysis .....................................//




//..................................................... Login ............................................... //
app.post('/api/login', (req, res) => {
  const { name, apikey } = req.body;

  if (!name || !apikey) {
    return res.status(400).json({ message: "Name and API key are required." });
  }

  const python = spawn('python', ['API-KeyDatabase.py', name, apikey]);

  let output = '';
  let errorOutput = ''; 

  python.stdout.on('data', (data) => {
    output += data.toString();
  });

  python.stderr.on('data', (data) => {
    errorOutput += data.toString(); 
  });

  python.on('close', (code) => {
    console.log(`Python script finished with code: ${code}`);
    console.log("Standard Output: ", output);
    console.log("Error Output: ", errorOutput);

    if (output.includes("success")) {
      res.json({ message: "Login successful!" });
    } else {
      res.json({ message: "Login failed. Please try again." });
    }
  });
});

//..................................................... Login ............................................... //


// .....................................................Start server............................................//
app.listen(PORT, () => {
  console.log(`🚀 Server running on http://localhost:${PORT}`);
});
