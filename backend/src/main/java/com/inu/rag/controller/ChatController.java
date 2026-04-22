package com.inu.rag.controller;

import com.inu.rag.service.AiService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/api/chat")
@CrossOrigin(origins = "*")
public class ChatController {

    @Autowired
    private AiService aiService;

    @PostMapping("/ask")
    public ResponseEntity<Map<String, Object>> askQuestion(@RequestBody Map<String, String> request) {
        String question = request.get("question");
        if (question == null || question.isEmpty()) {
            return ResponseEntity.badRequest().body(Map.of("error", "Question is required"));
        }

        try {
            Map<String, Object> result = aiService.askQuestion(question);
            return ResponseEntity.ok(result);
        } catch (Exception e) {
            return ResponseEntity.status(500).body(Map.of("error", e.getMessage()));
        }
    }
}
