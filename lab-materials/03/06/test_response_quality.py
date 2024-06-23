from llm_usage import infer_with_template, similarity_metric
import json


def test_response_quality():
    with open('example_text.txt') as f:
        input_text = f.read()
        
    with open('summary_template.txt') as f:
        template = f.read()

    expected_response = """- 事故報告をしたい\n- 相手の保険会社はXYZ保険会社であるn- 事故は2023年10月15日午後2時30分頃に起きたn- 交通状況は穏やかで、全方向に車両が走行していたn- 私はホンダ・アコードを運転していて、相手方はフォード・エスケープを運転していたn- 相手方の保険情報と連絡先情報を提供できるn- 写真を提供できる"""

    response = infer_with_template(input_text, template)
    print(f"Response: {response}")
    
    similarity = similarity_metric(response, expected_response)
    print(similarity)

    if similarity <= 0.8:
        raise Exception("Output is not similar enough to expected output")
        
    print("Response Quality OK")

    with open("quality_result.json", "w") as f:
        json.dump({
            "quality_test_response": response,
            "quality_test_similarity": similarity
        }, f)

if __name__ == '__main__':
    test_response_quality()