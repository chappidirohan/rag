package com.inu.rag.controller;

import com.inu.rag.model.Document;
import com.inu.rag.repository.DocumentRepository;
import com.inu.rag.service.AiService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/documents")
@CrossOrigin(origins = "*")
public class DocumentController {

    @Autowired
    private AiService aiService;

    @Autowired
    private DocumentRepository documentRepository;

    @GetMapping
    public List<Document> getDocuments() {
        return documentRepository.findAll();
    }

    @PostMapping("/upload")
    public ResponseEntity<?> uploadDocument(@RequestParam("file") MultipartFile file) {
        try {
            // 1. Upload to AI Service
            Map<String, Object> result = aiService.uploadDocument(file);
            String fileId = (String) result.get("file_id");

            // 2. Save metadata to PostgreSQL
            Document doc = new Document(fileId, file.getOriginalFilename(), LocalDateTime.now());
            documentRepository.save(doc);

            return ResponseEntity.ok(doc);
        } catch (Exception e) {
            return ResponseEntity.internalServerError().body(Map.of("error", e.getMessage()));
        }
    }
}
