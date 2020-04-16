package ugr.cc.airflow.controller;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.apache.commons.math3.util.Precision;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;
import ugr.cc.airflow.model.ByCityIdResponse;
import ugr.cc.airflow.model.Main;
import ugr.cc.airflow.model.Prediction;

import java.util.ArrayList;
import java.util.List;

@RestController
@RequestMapping(value = "/servicio/v2/prediccion")
public class PredictionController {

    private final String OPEN_WEATHER_API_KEY = "9f3bf94165f29a6f6380d31134cd2455";

    private final String SAN_FRANCISCO_ID = "5391959";

    private final String OPEN_WEAHTER_URL = "http://api.openweathermap.org/data/2.5/forecast";


    @RequestMapping(value = "/24horas",
            method = RequestMethod.GET,
            produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<Object> twentyFourHrs() {

        String result = getStringResponse();
        System.out.println(result);

        return getObjectResponseEntity(result, 8);
    }

    @RequestMapping(value = "/48horas",
            method = RequestMethod.GET,
            produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<Object> fortyEightHrs() {

        String result = getStringResponse();
        System.out.println(result);

        return getObjectResponseEntity(result, 16);
    }

    @RequestMapping(value = "/72horas",
            method = RequestMethod.GET,
            produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<Object> seventyTwoHrs() {

        String result = getStringResponse();
        System.out.println(result);

        return getObjectResponseEntity(result, 24);
    }

    private List<Prediction> parseResponse(ByCityIdResponse byCityIdResponse, int elements) {
        ArrayList<Prediction> predictions = new ArrayList<>(elements);
        int i = 0;
        ArrayList<ugr.cc.airflow.model.List> list =
                (ArrayList<ugr.cc.airflow.model.List>) byCityIdResponse.getList();

        while (i < elements) {
            Prediction prediction = new Prediction();
            ugr.cc.airflow.model.List listElement = list.get(i);
            Main main = listElement.getMain();
            prediction.setHour(listElement.getDtTxt());
            prediction.setHumidity(main.getHumidity());
            prediction.setTemperature(Precision.round(main.getTemp() - 273.15, 2));

            predictions.add(prediction);
            i++;
        }
        return predictions;
    }

    private String getStringResponse() {
        RestTemplate restTemplate = new RestTemplate();
        String uri =
                OPEN_WEAHTER_URL.concat("?id=").concat(SAN_FRANCISCO_ID).concat("&appid=").concat(OPEN_WEATHER_API_KEY);
        return restTemplate.getForObject(uri, String.class);
    }

    private ResponseEntity<Object> getObjectResponseEntity(String result, Integer elements) {
        try {
            ObjectMapper mapper = new ObjectMapper();
            ByCityIdResponse response = mapper.readValue(result, ByCityIdResponse.class);
            List<Prediction> predictions = parseResponse(response, elements);
            return new ResponseEntity<>(predictions, null, HttpStatus.OK);
        } catch (JsonProcessingException e) {
            e.printStackTrace();
            return new ResponseEntity<>("A problem occurred contacting API", null, HttpStatus.OK);
        }
    }

}
