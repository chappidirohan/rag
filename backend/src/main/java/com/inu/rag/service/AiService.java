package com.inu.rag.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.Resource;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.multipart.MultipartFile;

import java.util.HashMap;
import java.util.Map;

@Service
public class AiService {

    @Autowired
    private RestTemplate restTemplate;

    @org.springframework.beans.factory.annotation.Value("${ai.service.url}")
    private String aiServiceUrl;

    public Map<String, Object> uploadDocument(MultipartFile file) {
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.MULTIPART_FORM_DATA);

        MultiValueMap<String, Object> body = new LinkedMultiValueMap<>();
        body.add("file", file.getResource());

        HttpEntity<MultiValueMap<String, Object>> requestEntity = new HttpEntity<>(body, headers);

        ResponseEntity<Map> response = restTemplate.postForEntity(
                aiServiceUrl + "/process-document",
                requestEntity,
                Map.class);

        return response.getBody();
    }

    public Map<String, Object> askQuestion(String question) {
        Map<String, Object> request = new HashMap<>();
        request.put("query", question);
        request.put("top_k", 3);

        ResponseEntity<Map> response = restTemplate.postForEntity(
                aiServiceUrl + "/query",
                request,
                Map.class);
        return response.getBody();
    }
}
